from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, reverse
from .models import Course, CourseStudent
from django.contrib import messages


class CourseListView(ListView):
    template_name = 'courses/list.html'
    paginate_by = 12
    model = Course


class StudentCourseListView(CourseListView):
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
