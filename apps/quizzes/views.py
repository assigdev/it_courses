from django.shortcuts import render
from .models import Quiz, QuizResult
from django.views.generic import DetailView
from apps.course_users.mixins import StudentRequiredMixin


class QuizDetailView(StudentRequiredMixin, DetailView):
    model = Quiz

    def post(self, *args, **kwargs):
        quiz = Quiz.objects.get(slug=kwargs['slug'])
        quiz_result, __ = QuizResult.objects.get_or_create(quiz=quiz)
        quiz_result.save_result(self.request.POST)
        student_in_lesson = quiz.lesson.get_student_in_lesson(self.request.user.student)
        student_in_lesson.set_quiz_result(quiz_result)
        context = {
            'student_in_lesson': student_in_lesson,
            'quiz': quiz,
            'quiz_result': quiz_result
        }
        return render(self.request, 'quizzes/result.html', context)
