from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.courses.models import Course
from apps.main.mixins import HeaderMixin
from .forms import StudentForm
from .mixins import StudentRequiredMixin
from .models import Teacher, Student


class TeacherListView(HeaderMixin, ListView):
    template_name = 'course_users/teachers.html'
    paginate_by = 12
    model = Teacher
    header_path = 'course'

    def get_queryset(self):
        return super().get_queryset().select_related('user')


class TeacherDetailView(HeaderMixin, DetailView):
    model = Teacher
    template_name = 'course_users/teacher.html'
    header_path = 'course'

    def get_object(self, queryset=None):
        return super().get_queryset().get(user__username=self.kwargs['username'])


class StudentCreateView(StudentRequiredMixin, CreateView):
    form_class = StudentForm
    template_name = 'course_users/create_student.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка валидации')
        return super().form_invalid(form)

    def get_success_url(self):
        course_id = self.request.GET.get('course_id', False)
        messages.success(self.request, 'Профиль студента успешно создан. Теперь Вы можете записаться на курсы.')
        if course_id:
            slug = Course.objects.get(pk=course_id).slug
            return reverse('courses:detail', kwargs={'slug': slug})
        else:
            return reverse('courses:list')


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StudentForm
    template_name = 'course_users/update_student.html'

    def get_object(self, queryset=None):
        return self.request.user.student

    def get_success_url(self):
        messages.success(self.request, 'Профиль студента успешно изменен')
        return reverse('accounts:settings')


class StudentListView(HeaderMixin, ListView):
    template_name = 'course_users/student_list.html'
    model = Student
    paginate_by = 30
    header_path = 'course'
