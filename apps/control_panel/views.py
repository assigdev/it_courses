from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.course_users.mixins import TeacherRequiredMixin
from apps.courses.mixins import AjaxFormMixin
from apps.courses.models import Course
from apps.courses.models import Lesson
from apps.main.mixins import SecondHeaderMixin
from .forms import SelectionForm, VisitForm, HomeworkForm


class BaseCPDetailView(SecondHeaderMixin, AjaxFormMixin, DetailView):
    header_path = 'control'


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
        context['lesson'] = self._get_lesson(slug)
        return context

    def _get_lesson(self, slug):
        if slug is None:
            return self.get_object().lessons.get_current_lesson()
        return get_object_or_404(Lesson, slug=slug)


class StudentHomeworkCPView(StudentVisitCPView):
    template_name = 'control_panel/student_homework.html'
    url_name = 'control:homework_current'
    menu_title = 'Домашние задания'
    success_message = 'Изменения приняты'
    form = HomeworkForm
