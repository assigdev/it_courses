from django.urls import path
from .views import QuizDetailView, QuizResultView


app_name = 'quizzes'
urlpatterns = [
    path('quiz/<slug:slug>', QuizDetailView.as_view(), name='detail'),
    path('quiz/<slug:slug>/result/', QuizResultView.as_view(), name='result'),
]
