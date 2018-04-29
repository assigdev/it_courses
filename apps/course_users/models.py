from django.db import models
from django.conf import settings
from utils.shortcuts.for_stdimage import img_files_del
from stdimage import StdImageField
from utils.img_paths import get_img_path
from ckeditor_uploader.fields import RichTextUploadingField


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    img = StdImageField(
        "Фотография",
        upload_to=get_img_path,
        variations={'thumb': (400, 225, True)},
        blank=True
    )
    biography = RichTextUploadingField("Биография")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return "Преподаватель %s" % self.user.get_full_name()

    def get_finish_course_count(self):
        return self.course_set.filter(state='close').count()

    def get_first_course(self):
        return self.course_set.exclude(state='close').first()


img_files_del(Teacher)

SOCIAL_STATUS = (
    ('sc', 'Школьник'),
    ('st', 'Студент'),
    ('wo', 'Работаю'),
)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    social_status = models.CharField('Социальный статус', max_length=2, choices=SOCIAL_STATUS)
    school = models.CharField("Место учебы/работы", max_length=100)
    parent_phone = models.CharField("Телефонный номер родителя", max_length=20)
    homework_count = models.PositiveSmallIntegerField('Количество сданных ДЗ', default=0)
    quiz_count = models.PositiveSmallIntegerField('Количество сданных тестов', default=0)
    score = models.PositiveIntegerField('Количество баллов', default=0)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студент"
        ordering = ['-score']

    def __str__(self):
        return self.user.get_full_name()

    def get_open_curses(self):
        return self.course_set.filter(coursestudent__status__in=('active', 'finish'))

    def get_first_course(self):
        return self.get_open_curses().first()

    def get_lessons_count(self):
        return self.studentinlesson_set.filter(attendance=True).count()

    def get_finish_courses(self):
        return self.course_set.filter(state='finish').count()
