from django.urls import path
from .views import TeacherDetailView, TeacherListView, StudentCreateView, StudentUpdateView, StudentListView


app_name = 'course_users'
urlpatterns = [
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('teachers/<username>', TeacherDetailView.as_view(), name='teacher'),
    path('create_student/', StudentCreateView.as_view(), name='create_student'),
    path('update_student/', StudentUpdateView.as_view(), name='update_student'),
    path('students/', StudentListView.as_view(), name='students'),

]
