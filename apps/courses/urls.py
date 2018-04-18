from django.urls import path, include
from .views import CourseListView, CourseDetailView, StudentCourseListView, course_enroll


app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('my_courses/', StudentCourseListView.as_view(), name='my_courses'),
    path('<slug:slug>', CourseDetailView.as_view(), name='detail'),
    path('users/', include('apps.course_users.urls', namespace="users")),
    path('enroll/<slug:slug>', course_enroll, name="enroll"),

]
