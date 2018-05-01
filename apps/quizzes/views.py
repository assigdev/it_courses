from django.shortcuts import reverse, redirect, Http404
from .models import Quiz, QuizResult
from django.views.generic import DetailView, TemplateView
from apps.course_users.mixins import StudentRequiredMixin
from django.core.exceptions import ObjectDoesNotExist


class QuizDetailView(StudentRequiredMixin, DetailView):
    model = Quiz

    def post(self, *args, **kwargs):
        quiz = Quiz.objects.get(slug=kwargs['slug'])
        quiz_result = QuizResult.objects.create(quiz=quiz)
        quiz_result.save_result(self.request.POST)
        student_in_lesson = quiz.lesson.get_student_in_lesson(self.request.user.student)
        student_in_lesson.set_quiz_result(quiz_result)
        return redirect(reverse('quiz:result', kwargs={'slug': quiz.slug}))


class QuizResultView(StudentRequiredMixin, DetailView):
    template_name = 'quizzes/result.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        try:
            student_in_lesson = quiz.lesson.get_student_in_lesson(self.request.user.student)
            quiz_result = QuizResult.objects.get(quiz=quiz, studentinlesson=student_in_lesson)
            context['quiz_result'] = quiz_result
            context['results'] = zip(quiz.questions.all(), quiz_result.studentanswer_set.all())
        except ObjectDoesNotExist:
            raise Http404
        return context
