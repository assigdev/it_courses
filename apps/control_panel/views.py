from django.shortcuts import render
from django.views.generic import DetailView
from apps.course_users.models import Teacher
from apps.course_users.mixins import TeacherRequiredMixin
from .mixins import SecondHeaderMixin
from apps.courses.models import Course
from django.http import JsonResponse
from .forms import SelectionForm


class AjaxDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.get_ajax_response()
        return super().get(request, *args, **kwargs)

    def get_ajax_response(self):
        ajax_context = self.get_ajax_context_data()
        return JsonResponse(ajax_context)

    def get_ajax_context_data(self):
        return {'error': None}


# CP is Control Panel
class StudentSelectionCPView(SecondHeaderMixin, TeacherRequiredMixin, AjaxDetailView):
    model = Course
    template_name = 'control_panel/student_selection.html'
    url_name = ''
    menu_title = 'Статус'

    def get_queryset(self):
        return super().get_queryset().filter(teachers=self.request.user.teacher).prefetch_related('students')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu_courses'] = self.get_queryset()
        return context

    def get_ajax_context_data(self):
        context = super().get_ajax_context_data()
        form = SelectionForm(self.request.GET)
        if form.is_valid():
            form.save()
            context['message'] = 'Статус успешно изменен'
        else:
            print(form)
            context['error'] = 'Отправленны не валидные данные'
        return context


# CP is Control Panel
class StudentVisitCPView(SecondHeaderMixin, TeacherRequiredMixin, AjaxDetailView):
    model = Course
    template_name = 'control_panel/student_visit.html'
    url_name = ''
    menu_title = 'Посещения'

    def get_queryset(self):
        return super().get_queryset().filter(teachers=self.request.user.teacher).prefetch_related('students')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_ajax_context_data(self):
        context = super().get_ajax_context_data()
        form = SelectionForm(self.request.GET)
        if form.is_valid():
            form.save()
            context['message'] = 'Статус успешно изменен'
        else:
            print(form)
            context['error'] = 'Отправленны не валидные данные'
        return context
