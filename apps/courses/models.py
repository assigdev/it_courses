from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db import transaction
from django.utils import timezone
from stdimage import StdImageField

from apps.course_users.models import Teacher, Student
from apps.quizzes.models import Quiz
from apps.quizzes.models import QuizResult
from it_courses.settings import LEVEL, HOMEWORK_SCORE, TEST_SCORE, ATTENDANCE_SCORE, DEADLINE_COEFFICIENT
from utils.img_paths import get_img_path
from utils.shortcuts.for_stdimage import img_files_del

STATES = (
    ('active', 'Курс уже идет'),
    ('close', 'Курс окончен'),
    ('reg', 'Открыт набор на курс'),
)


class Course(models.Model):
    title = models.CharField('Название', max_length=100)
    img = StdImageField(
        "Фотография",
        upload_to=get_img_path,
        variations={'thumb': (400, 225, True)},
        blank=True
    )
    slug = models.SlugField(max_length=20)
    state = models.CharField('статус', choices=STATES, max_length=6)
    max_user_count = models.PositiveSmallIntegerField('Максимальное количество учащихся')
    about = RichTextUploadingField('Описание курса')
    teachers = models.ManyToManyField(Teacher, verbose_name='Учителя')
    students = models.ManyToManyField(Student, verbose_name='Студенты', through='CourseStudent')
    duration = models.CharField('Продолжительность курса', max_length=20)
    start_date = models.DateField('Дата начала курса')
    end_date = models.DateField('Дата завершения курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_lesson_count(self):
        return "%s занятий" % self.lessons.count()


COURSE_STATUS = (
    ('in_view', "На собеседовании"),
    ('active', 'Вам доступен этот курс'),
    ('fail', "Исключен из курса"),
    ('fail_view', "Не прошел собеседование"),
    ('finish', "Окончил курс"),
)


class CourseStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField("Статус", max_length=9, choices=COURSE_STATUS)

    def get_marker(self):
        return {
            'in_view': 'badge-primary',
            'active': 'badge-primary',
            'fail': 'badge-danger',
            'fail_view': 'badge-danger',
            'finish': 'badge-success',
        }.get(self.status, '')

    def get_status_options(self):
        html = ''
        option = '<option value="%s" %s>%s</option>'
        for status in COURSE_STATUS:
            selected = 'selected' if status[0] == self.status else ''
            html += option % (status[0], selected, status[1])
        return html


class LessonQuerySet(models.QuerySet):
    def get_current_lesson(self):
        current = self.filter(date__gte=timezone.now()).first()
        return current or self.last()


class Lesson(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=20, blank=True)
    course = models.ForeignKey(Course, 'Курс', related_name='lessons')
    number = models.PositiveSmallIntegerField('Номер занятия', default=1)
    date = models.DateField('Дата занятия', default=timezone.now)
    content = RichTextUploadingField('Материал занятия', blank=True)
    homework = RichTextUploadingField('Домашнее задание', blank=True)
    homework_level = models.PositiveSmallIntegerField('Уровень сложности Домашней Работы', choices=LEVEL, default=3)
    homework_deadline = models.DateField('Дедлайн для домашней работы', blank=True, null=True)
    quiz = models.OneToOneField(Quiz, verbose_name='Тестирование', default=None, blank=True, null=True,
                                on_delete=models.SET_NULL)
    quiz_deadline = models.DateField('Дедлайн для тестирования', blank=True, null=True)

    objects = LessonQuerySet.as_manager()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['number']

    def have_homework(self):
        if len(self.homework) < 10:
            return False
        return True

    def have_homework_word(self):
        return "Да" if self.have_homework() else "Нет"

    def have_quiz(self):
        if self.quiz is None:
            return False
        return True

    def have_quiz_word(self):
        return "Да" if self.have_quiz() else "Нет"

    def get_student_in_lesson(self, student):
        obj, __ = StudentInLesson.objects.get_or_create(student=student, lesson=self)
        return obj


QUIZ_STATUS = (
    ('on', 'Пройден'),
    ('off', 'Провален'),
    ('not_start', 'Не начат'),
)


class StudentInLesson(models.Model):
    student = models.ForeignKey(Student, verbose_name='ученик', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, verbose_name='Занятие', on_delete=models.CASCADE)
    attendance = models.BooleanField('Был на занятии', default=False)
    is_homework_final = models.BooleanField('ДЗ сдана', default=False)
    is_homework_in_deadline = models.NullBooleanField('ДЗ сдано в срок', default=None)
    homework_link = models.URLField('Ссылка на ДЗ', blank=True)
    quiz_status = models.CharField('Статус тестирования', max_length=9, default='not_start', choices=QUIZ_STATUS)
    is_quiz_in_deadline = models.NullBooleanField('Тест сдан в срок', default=None)
    quiz_result = models.OneToOneField(QuizResult, 'Результат тестирования', default=None, blank=True, null=True)
    homework_score = models.PositiveSmallIntegerField('Очки за домашнее задание', default=0)
    quiz_score = models.PositiveSmallIntegerField('Очки за тестирование', default=0)

    class Meta:
        verbose_name = 'Студент на занятии'
        verbose_name_plural = 'Студенты на занятиях'

    @transaction.atomic
    def set_quiz_result(self, quiz_result):
        quiz = quiz_result.quiz
        result_percent = quiz_result.get_result_percent()
        student = self.student

        if self.lesson.quiz_deadline and self.lesson.quiz_deadline > timezone.now().date():
            self.is_quiz_in_deadline = True
            deadline_coefficient = DEADLINE_COEFFICIENT
        else:
            self.is_quiz_in_deadline = False
            deadline_coefficient = 1
        if quiz.result > result_percent:
            self.quiz_status = 'off'
            coefficient = 0.5
        else:
            self.quiz_status = 'on'
            coefficient = 1
        self.quiz_score = int(TEST_SCORE * quiz.level * deadline_coefficient * coefficient * result_percent / 100)
        self.quiz_result = quiz_result
        self.save()
        student.score += self.quiz_score
        student.save()

    @transaction.atomic
    def set_homework_result(self, is_final):
        if self.lesson.homework_deadline and self.lesson.homework_deadline > timezone.now().date():
            self.is_homework_in_deadline = True
            deadline_coefficient = DEADLINE_COEFFICIENT
        else:
            self.is_homework_in_deadline = False
            deadline_coefficient = 1
        self.is_homework_final = is_final
        student = self.student
        if is_final:
            self.homework_score = HOMEWORK_SCORE * self.lesson.homework_level * deadline_coefficient
            student.score += self.homework_score
            student.homework_count += 1
        else:
            self.homework_score = 0
            student.score -= HOMEWORK_SCORE * self.lesson.homework_level * deadline_coefficient
            student.homework_count -= 1
        student.save()
        self.save()

    @transaction.atomic
    def set_attendance(self, is_attendance):
        self.attendance = is_attendance
        student = self.student
        if is_attendance:
            student.score += ATTENDANCE_SCORE
        else:
            student.score -= ATTENDANCE_SCORE
        student.save()
        self.save()

    def get_attendance(self):
        return {
            False: 'Не был',
            True: 'Был на занятии',
        }[self.attendance]

    def get_homework_final(self):
        return {
            True: 'Сдано',
            False: 'Не сдано',
        }[self.is_homework_final]

    def get_homework_in_deadline(self):
        return {
            False: 'Нет',
            True: 'Да',
            None: 'Еще не сдана',
        }[self.is_homework_in_deadline]

    def get_quiz_in_deadline(self):
        return {
            False: 'Нет',
            True: 'Да',
            None: 'Тест не начат',
        }[self.is_quiz_in_deadline]

    def checked_homework_final(self):
        if self.is_homework_final:
            return 'checked'
        return ''

    def checked_attendance(self):
        if self.attendance:
            return 'checked'
        return ''


img_files_del(Course)
