from django.db import models
from apps.course_users.models import Teacher, Student
from apps.quizzes.models import Quiz
from martor.models import MartorField
from django.utils import timezone
from utils.mixins.models import ModelAutoSlugMixin
from apps.quizzes.models import QuizResult
from utils.shortcuts.for_stdimage import img_files_del
from stdimage import StdImageField
from utils.img_paths import HASH_CHUNK_SIZE

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
    about = MartorField('Описание курса')
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


class Lesson(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=20, blank=True)
    course = models.ForeignKey(Course, 'Курс', related_name='lessons')
    number = models.PositiveSmallIntegerField('Номер занятия', default=1)
    date = models.DateField('Дата занятия', default=timezone.now)
    content = MartorField('Материал занятия', blank=True)
    home_work = MartorField('Домашнее задание', blank=True)
    home_work_deadline = models.DateField('Дедлайн для домашней работы', blank=True, null=True)
    quiz = models.ForeignKey(Quiz, verbose_name='Тестирование', blank=True, null=True, on_delete=models.SET_NULL)
    quiz_deadline = models.DateField('Дедлайн для тестирования', blank=True, null=True)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


QUIZ_STATUS = (
    ('on_first', 'Пройден с первого раза'),
    ('on_second', 'Пройден со второго раза'),
    ('on_third', 'Пройден со третьего раза'),
    ('off_first', 'Не пройден с первого раза'),
    ('off_second', 'Не пройден со второго раза'),
    ('off', 'Провален'),
    ('not_start', 'Не начат'),
)


class StudentInLesson(models.Model):
    student = models.ForeignKey(Student, verbose_name='ученик', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, verbose_name='Занятие', on_delete=models.CASCADE)
    attendance = models.BooleanField('Был на занятии', default=True)
    is_homework_final = models.BooleanField('Сдана', default=False)
    is_homework_in_deadline = models.NullBooleanField('В срок', default=None)
    quiz_status = models.CharField('Статус тестирования', max_length=9, choices=QUIZ_STATUS)
    is_quiz_in_deadline = models.NullBooleanField('В срок', default=None)
    quiz_result = models.ForeignKey(QuizResult, 'Результат тестирования')

    class Meta:
        verbose_name = 'Студент на занятии'
        verbose_name_plural = 'Студенты на занятиях'

    def __str__(self):
        return ''


img_files_del(Course)
