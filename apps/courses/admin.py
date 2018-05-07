from django.contrib import admin
from .models import Course, Lesson, CourseStudent


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'max_user_count', 'duration', 'start_date', 'end_date')


@admin.register(Lesson)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'number', 'date', 'homework_deadline', 'quiz_deadline')


@admin.register(CourseStudent)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status')
