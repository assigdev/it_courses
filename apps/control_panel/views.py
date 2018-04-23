from django.views.generic import DetailView
from apps.course_users.mixins import TeacherRequiredMixin
from apps.main.mixins import SecondHeaderMixin
from apps.courses.models import Course
from django.http import JsonResponse
from .forms import SelectionForm, VisitForm, HomeworkForm


class BaseCPDetailView(SecondHeaderMixin, DetailView):
    success_message = ''
    form = None
    header_path = 'control'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.get_ajax_response()
        return super().get(request, *args, **kwargs)

    def get_ajax_response(self):
        ajax_context = self.get_ajax_context_data()
        return JsonResponse(ajax_context)

    def get_ajax_context_data(self):
        context = {'is_error': False}
        form = self.form(self.request.GET)
        if form.is_valid():
            form.save()
            context['message'] = self.success_message
        else:
            context['message'] = 'Отправленны не валидные данные'
            context['is_error'] = True
        return context

    def get_object(self, queryset=None):
        if self.kwargs['slug'] == 'base':
            return self.get_queryset().first()
        return super().get_object(queryset=queryset)


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
    url_name = 'control:visit'
    menu_title = 'Посещения'
    success_message = 'Изменения приняты'
    form = VisitForm

    def get_queryset(self):
        return super().get_queryset().filter(teachers=self.request.user.teacher).prefetch_related('students')


class StudentHomeworkCPView(StudentSelectionCPView):
    template_name = 'control_panel/student_visit.html'
    url_name = 'control_panel:homework'
    menu_title = 'Домашние задания'
    success_message = 'Изменения приняты'
    form = HomeworkForm

    def get_queryset(self):
        return super().get_queryset().filter(teachers=self.request.user.teacher).prefetch_related('students')

