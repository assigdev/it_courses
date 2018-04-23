from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from it_courses.settings import SITE_URL
from .tokens import account_activation_token
from django.core.exceptions import ObjectDoesNotExist


class ITUser(AbstractUser):
    phone = models.CharField("Телефонный номер", max_length=20)
    birthday = models.DateField("День рождения")
    email = models.EmailField("email", unique=True)
    email_confirmed = models.BooleanField("Почта подтверждена", default=False)

    REQUIRED_FIELDS = ['email', 'phone', 'birthday']

    def send_activation_email(self):
        subject = 'Подтвердите почту для продолжения работы на ITCourses.'
        message = render_to_string('emails/account_activation_email.html', {
            'user': self,
            'domain': SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)).decode('unicode_escape'),
            'token': account_activation_token.make_token(self),
        })
        self.email_user(subject, message)

    def is_student(self):
        try:
            if self.student:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def is_teacher(self):
        try:
            if self.teacher:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def is_active_student(self):
        if self.is_student():
            if self.student.get_open_curses().count() > 0:
                return True
        return False
