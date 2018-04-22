"""it_courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from it_courses import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('apps.accounts.urls', namespace="accounts")),
    path('education/', include('apps.courses.urls', namespace="courses")),
    path('control_panel/', include('apps.control_panel.urls', namespace='control')),
    path('quiz/', include('apps.quizzes.urls', namespace='quiz')),

    path('admin/', admin.site.urls),
    path('verified-email-field/', include('verified_email_field.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('_nested_admin/', include('nested_admin.urls')),

    path('', include('apps.main.urls', namespace="main")),

]

if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
