# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MY_APPS = [
    'apps.main',
    'apps.course_users',
    'apps.courses',
    'apps.control_panel',
    'apps.quizzes',
    'apps.accounts',
]


INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'nested_admin',
]

DEV_APS = [

]

PROD_APS = [
    'raven.contrib.django.raven_compat',
]

INSTALLED_APPS = DJANGO_APPS + INSTALLED_APPS + MY_APPS
