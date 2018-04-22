from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import reverse


class TeacherRequiredMixin(AccessMixin):
    permission_denied_message = 'Для доступа к этой странице вам необходимо быть преподавателем. Зайдите из под ' \
                                'аккаунта с профилем преподавателя'

    """Verify that the current user is teacher."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            messages.warning(request, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(AccessMixin):
    permission_denied_message = 'Вы не являетесь студентом, пожалуйста зарегистрируйтесь как студент.'

    """Verify that the current user is student"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Пожалуйста авторизуйтесь для доступа к данной странице')
            return self.handle_no_permission()
        if not request.user.is_student:
            self.login_url = reverse('courses:users:create_student')
            messages.warning(request, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
