from django.urls import path, include
from .views import (
    CourseListView,
    CourseDetailView,
    StudentCourseListView,
    course_enroll,
    LessonListView,
    LessonDetailView
 )


app_name = 'courses'
urlpatterns = [
    path('courses/', CourseListView.as_view(), name='list'),
    path('my_courses/', StudentCourseListView.as_view(), name='my_courses'),
    path('lessons/<slug:slug>', LessonListView.as_view(), name='lessons'),
    path('lessons/<slug:slug>/<slug:lesson_slug>', LessonDetailView.as_view(), name='lesson'),
    path('courses/<slug:slug>', CourseDetailView.as_view(), name='detail'),
    path('users/', include('apps.course_users.urls', namespace="users")),
    path('enroll/<slug:slug>', course_enroll, name="enroll"),

]
