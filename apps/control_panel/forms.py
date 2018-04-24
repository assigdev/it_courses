from django import forms
from apps.course_users.models import Student
from apps.courses.models import COURSE_STATUS, CourseStudent, Course, Lesson, StudentInLesson
from django.shortcuts import get_object_or_404


class SelectionForm(forms.Form):
    course_id = forms.IntegerField(required=True)
    student_id = forms.IntegerField(required=True)
    status = forms.ChoiceField(choices=COURSE_STATUS)

    def save(self):
        course_id = self.cleaned_data['course_id']
        student_id = self.cleaned_data['student_id']
        status = self.cleaned_data['status']
        obj = get_object_or_404(CourseStudent, student__id=student_id, course__id=course_id)
        obj.status = status
        obj.save()
        return obj


class VisitForm(forms.Form):
    lesson_id = forms.IntegerField(required=True)
    student_id = forms.IntegerField(required=True)
    attendance = forms.BooleanField(required=False)

    def save(self):
        lesson_id = self.cleaned_data['lesson_id']
        student_id = self.cleaned_data['student_id']
        attendance = self.cleaned_data['attendance']
        obj = StudentInLesson.objects.get(lesson__id=lesson_id, student__id=student_id)
        obj.set_attendance(attendance)
        return obj


class HomeworkForm(forms.Form):
    lesson_id = forms.IntegerField(required=True)
    student_id = forms.IntegerField(required=True)
    is_homework_final = forms.BooleanField(required=False)

    def save(self):
        lesson_id = self.cleaned_data['lesson_id']
        student_id = self.cleaned_data['student_id']
        is_homework_final = self.cleaned_data['is_homework_final']
        obj = StudentInLesson.objects.get(lesson__id=lesson_id, student__id=student_id)
        obj.set_homework_result(is_homework_final)
        return obj
