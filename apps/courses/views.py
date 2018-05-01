from django.contrib import messages
from django.shortcuts import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from apps.course_users.mixins import StudentRequiredMixin
from apps.main.mixins import HeaderMixin
from apps.main.mixins import SecondHeaderMixin
from .forms import HomeworkLinkForm
from .mixins import AjaxFormMixin
from .models import Course, CourseStudent, Lesson


class CourseListView(HeaderMixin, ListView):
    template_name = 'courses/list.html'
    paginate_by = 12
    model = Course
    header_path = 'course'


class StudentCourseListView(StudentRequiredMixin, CourseListView):
    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user.student)


class CourseDetailView(HeaderMixin, DetailView):
    template_name = 'courses/detail.html'
    model = Course
    context_object_name = 'course'
    header_path = 'course'


def course_enroll(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        course = None
    if not course or not request.user.is_student:
        messages.error(request, 'Ошибка при записи на курс')
        return redirect('courses:list')
    CourseStudent.objects.create(course=course, student=request.user.student, status='in_view')
    course = Course.objects.get(pk=request.GET.get('course_id', 1))
    messages.success(request, "Вы успешно записались на курс")
    return redirect('courses:detail', course.slug)


class LessonListView(SecondHeaderMixin, AjaxFormMixin, StudentRequiredMixin, ListView):
    model = Lesson
    template_name = 'courses/lessons.html'
    menu_title = 'Занятия'
    url_name = 'courses:lessons'
    header_path = 'lesson'
    success_message = 'Ссылка успешно сохранена'
    form = HomeworkLinkForm

    def get_queryset(self):
        return super().get_queryset().filter(course__slug=self.kwargs['slug'])

    def get_menu_queryset(self):
        return self.request.user.student.get_open_curses()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['current_lesson'] = self.get_queryset().get_current_lesson()
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
