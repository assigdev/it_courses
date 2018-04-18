from django.urls import path, re_path
from .views import SignUpView, AccountUpdateView, logout_view, activate, send_activation_email
from django.contrib.auth.views import LoginView


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    re_path(
        r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate,
        name='activate'
    ),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('send_activation_email/', send_activation_email, name='send_activation_email'),
    path('settings/', AccountUpdateView.as_view(), name='settings'),
]
