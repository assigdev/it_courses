from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, reverse
from .models import Course, CourseStudent, Lesson
from django.contrib import messages
from apps.course_users.mixins import StudentRequiredMixin
from django.utils import timezone
from apps.control_panel.mixins import SecondHeaderMixin
from django.shortcuts import Http404

class CourseListView(ListView):
    template_name = 'courses/list.html'
    paginate_by = 12
    model = Course


class StudentCourseListView(StudentRequiredMixin, CourseListView):
    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user.student)


class CourseDetailView(DetailView):
    template_name = 'courses/detail.html'
    model = Course
    context_object_name = 'course'


def course_enroll(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        course = None
    if not course or not request.user.is_student:
        messages.error(request, 'Ошибка при записи на курс')
        return redirect('courses:list')
    course_student = CourseStudent(course=course, student=request.user.student)
    if course.selection_test is None:
        course_student.status = 'in_view'
    else:
        course_student.status = ''
    course_student.save()
    course = Course.objects.get(pk=request.GET.get('course_id', 1))
    messages.success(request, "Вы успешно записались на курс")
    return redirect('courses:detail', course.slug)


class LessonListView(SecondHeaderMixin, ListView):
    model = Lesson
    template_name = 'courses/lessons.html'
    menu_title = 'Занятия'

    def get_queryset(self):
        return super().get_queryset().filter(course__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['current_lesson'] = self.get_queryset().get_current_lesson
        context['menu_courses'] = self.request.user.student.course_set.all()
        context['course_slug'] = self.kwargs['slug']

        return context


class LessonDetailView(LessonListView):
    template_name = 'courses/lesson.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        try:
            context['lesson'] = self.get_queryset().get(slug=self.kwargs['lesson_slug'])
        except Lesson.DoesNotExist:
            raise Http404
        return context
