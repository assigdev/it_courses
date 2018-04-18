from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import HttpResponseRedirect, reverse, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView

from .forms import SignUpForm, UserUpdateForm
from .tokens import account_activation_token


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        messages.info(self.request, 'Вы успешно зарегистрировались. Теперь вы можете войти.')
        return reverse("accounts:login")


class AccountUpdateView(UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/settings.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Данные успешно изменены')
        return reverse('accounts:settings')


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из акаунта')
    return HttpResponseRedirect('/')


def activate(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Вы успешно подтвердили почту!')
    else:
        messages.error(request, 'Ошибка при подтверждении почты, попробуйте еще раз')
    return redirect('main:home')


def send_activation_email(request):
    user = request.user
    user.send_activation_email()
    messages.info(request, 'Активация отправлена на почту')
    return redirect('main:home')
