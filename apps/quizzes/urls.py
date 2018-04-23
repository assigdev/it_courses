from django.urls import path
from .views import QuizDetailView


app_name = 'quizzes'
urlpatterns = [
    path('quiz/<slug:slug>', QuizDetailView.as_view(), name='detail'),
]
