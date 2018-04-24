from django.views.generic import DetailView
from apps.course_users.mixins import TeacherRequiredMixin
from apps.main.mixins import SecondHeaderMixin
from apps.courses.models import Course
from django.http import JsonResponse
from .forms import SelectionForm, VisitForm, HomeworkForm
from django.shortcuts import get_object_or_404
from apps.courses.models import Lesson


class BaseCPDetailView(SecondHeaderMixin, DetailView):
    success_message = ''
    form = None
    header_path = 'control'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.get_ajax_response()
        return super().get(request, *args, **kwargs)

    def get_ajax_response(self):
        ajax_context = self.get_ajax_context_data()
        return JsonResponse(ajax_context)

    def get_ajax_context_data(self):
        context = {'is_error': False}
        form = self.form(self.request.POST)
        print(form)
        if form.is_valid():
            form.save()
            context['message'] = self.success_message
        else:
            context['message'] = 'Отправленны не валидные данные'
            context['is_error'] = True
        return context

    def get_object(self, queryset=None):
        return super().get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        return context


class StudentSelectionCPView(TeacherRequiredMixin, BaseCPDetailView):
    model = Course
    template_name = 'control_panel/student_selection.html'
    url_name = 'control:selection'
    menu_title = 'Статус'
    success_message = 'Статус успешно сохранен'
    form = SelectionForm

    def get_queryset(self):
        return super().get_queryset().filter(teachers=self.request.user.teacher).prefetch_related('students')


class StudentVisitCPView(StudentSelectionCPView):
    template_name = 'control_panel/student_visit.html'
    url_name = 'control:visit_current'
    menu_title = 'Посещения'
    success_message = 'Изменения приняты'
    form = VisitForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('lesson_slug', None)
        if slug is None:
            context['lesson'] = self.get_object().lessons.get_current_lesson()
        else:
            context['lesson'] = get_object_or_404(Lesson, slug=slug)
        return context


class StudentHomeworkCPView(StudentVisitCPView):
    template_name = 'control_panel/student_homework.html'
    url_name = 'control:homework_current'
    menu_title = 'Домашние задания'
    success_message = 'Изменения приняты'
    form = HomeworkForm
