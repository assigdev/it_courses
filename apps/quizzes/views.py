from django.shortcuts import render
from .models import Quiz, QuizResult
from django.views.generic import DetailView


class QuizDetailView(DetailView):
    model = Quiz

    def post(self):
        # obj = Quiz.objects.get(slug=self.kwargs['slug'])
        # # quiz_result = QuizResult.objects.get_or_create()
        #
        # for question in obj.questions.all():

            # answer = self.request.POST['answer_%s' % question.position]
        print(1)
        return render(self.request, 'quizzes/result.html', {})