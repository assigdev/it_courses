from django.db import models
from django.conf import settings
from martor.models import MartorField
from utils.shortcuts.for_stdimage import img_files_del
from stdimage import StdImageField
from utils.img_paths import HASH_CHUNK_SIZE


def teacher_img_path(instance, filename):
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
        'teachers',
        hex_path[0:2],
        hex_path[2:18],
        hex_path[18:34],
        parts[1]
    )


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    img = StdImageField(
        "Фотография",
        upload_to=teacher_img_path,
        variations={'thumb': (400, 225, True)},
        blank=True
    )
    biography = MartorField("Биография")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return "Преподаватель %s" % self.user.get_full_name()

    def get_finish_course_count(self):
        return self.course_set.filter(state='close').count()


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
    score = models.PositiveIntegerField('Количество баллов', default=0)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студент"

    def __str__(self):
        return self.user.get_full_name()

    def get_open_curses(self):
        print(self.course_set.exclude(coursestudent__status__in=('fail', 'fail_view')))
        return self.course_set.exclude(coursestudent__status__in=('fail', 'fail_view'))
