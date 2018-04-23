from django.db import models
from apps.course_users.models import Teacher, Student
from apps.quizzes.models import Quiz
from django.utils import timezone
from apps.quizzes.models import QuizResult
from utils.shortcuts.for_stdimage import img_files_del
from stdimage import StdImageField
from utils.img_paths import HASH_CHUNK_SIZE
from ckeditor_uploader.fields import RichTextUploadingField
from it_courses.settings import LEVEL, HOMEWORK_SCORE, TEST_SCORE, ATTENDANCE_SCORE
from django.db import transaction


STATES = (
    ('active', 'Курс уже идет'),
    ('close', 'Курс окончен'),
    ('reg', 'Открыт набор на курс'),
)


def course_img_path(instance, filename):
    import os.path
    import hashlib
    parts = os.path.splitext(filename)
    ctx = hashlib.sha256()
    if instance.img.multiple_chunks():
        for data in instance.img.chunks(HASH_CHUNK_SIZE):
            ctx.update(data)
    else:
        ctx.update(instance.img.read())
    hex_path = ctx.hexdigest()
    return '{0}/{1}/{2}/{3}{4}'.format(
        'courses',
        hex_path[0:2],
        hex_path[2:18],
        hex_path[18:34],
        parts[1]
    )


class Course(models.Model):
    title = models.CharField('Название', max_length=100)
    img = StdImageField(
        "Фотография",
        upload_to=course_img_path,
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
    homework_level = models.PositiveSmallIntegerField('Уровень сложности', choices=LEVEL, default=3)
    homework_deadline = models.DateField('Дедлайн для домашней работы', blank=True, null=True)
    quiz = models.OneToOneField(Quiz, verbose_name='Тестирование', default=None,  blank=True, null=True, on_delete=models.SET_NULL)
    quiz_deadline = models.DateField('Дедлайн для тестирования', blank=True, null=True)

    objects = LessonQuerySet.as_manager()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def have_homework(self):
        if len(self.homework) > 10:
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
    ('off', 'Не пройден'),
    ('not_start', 'Не начат'),
)


class StudentInLesson(models.Model):
    student = models.ForeignKey(Student, verbose_name='ученик', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, verbose_name='Занятие', on_delete=models.CASCADE)
    attendance = models.BooleanField('Был на занятии', default=False)
    is_homework_final = models.BooleanField('Сдана', default=False)
    is_homework_in_deadline = models.NullBooleanField('В срок', default=None)
    quiz_status = models.CharField('Статус тестирования', max_length=9, default='not_start', choices=QUIZ_STATUS)
    is_quiz_in_deadline = models.NullBooleanField('В срок', default=None)
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
        if quiz.result > result_percent:
            self.quiz_status = 'off'
            coefficient = 0.5
        else:
            self.quiz_status = 'on'
            coefficient = 1
        self.quiz_score = int(TEST_SCORE * quiz.level * coefficient * result_percent / 100)
        self.is_quiz_in_deadline = False if self.lesson.quiz_deadline > timezone.now().date() else True
        self.quiz_result = quiz_result
        self.save()
        self.student.score += self.quiz_score
        self.student.save()

    @transaction.atomic
    def set_homework_result(self, is_final):
        self.is_homework_in_deadline = False if self.lesson.homework_deadline > timezone.now().date() else True
        self.is_homework_final = is_final
        if is_final:
            self.homework_score = HOMEWORK_SCORE * self.lesson.homework_level
            self.student.score += self.homework_score
            self.student.homework_count += 1
            self.student.save()
        else:
            self.homework_score = 0
            self.student.score -= HOMEWORK_SCORE * self.lesson.homework_level
            self.student.homework_count -= 1
            self.student.save()
        self.save()

    @transaction.atomic
    def set_attendance(self, is_attendance):
        self.attendance = is_attendance

    def get_attendance(self):
        return {
                False: 'Не был',
                True: 'Был на занятии',
            }[self.attendance]

    def get_homework_final(self):
        return {
                False: 'Сдано',
                True: 'Не сдано',
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
                None: 'Тест не пройден',
        }[self.is_homework_in_deadline]


img_files_del(Course)
