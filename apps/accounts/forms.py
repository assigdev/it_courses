from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'birthday',
            'email',
            'phone',
            'password1',
            'password2')
        widgets = {
            'birthday': DateInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        user.send_activation_email()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'birthday',
            'phone',
        )
        widgets = {
            'birthday': DateInput()
        }