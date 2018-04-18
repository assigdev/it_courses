from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'max_user_count', 'duration', 'start_date', 'end_date')


@admin.register(Lesson)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'number', 'date', 'home_work_deadline', 'quiz_deadline')
