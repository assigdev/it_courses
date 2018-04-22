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
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(Student, id=student_id)
        obj = get_object_or_404(CourseStudent, student=student, course=course)
        obj.status = status
        obj.save()
        return obj


class VisitForm(forms.Form):
    lesson_id = forms.IntegerField(required=True)
    student_id = forms.IntegerField(required=True)
    attendance = forms.BooleanField(required=True)

    def save(self):
        lesson_id = self.cleaned_data['lesson_id']
        student_id = self.cleaned_data['student_id']
        attendance = self.cleaned_data['attendance']
        # lesson = get_object_or_404(Course, id=lesson_id)
        # student = get_object_or_404(Student, id=student_id)
        obj = StudentInLesson.objects.get(lesson__id=lesson_id, student__id=student_id)
        obj.attendance = attendance
        obj.save()
        return obj


class HomeWorkForm(forms.Form):
    lesson_id = forms.IntegerField(required=True)
    student_id = forms.IntegerField(required=True)
    attendance = forms.BooleanField(required=True)

    def save(self):
        lesson_id = self.cleaned_data['lesson_id']
        student_id = self.cleaned_data['student_id']
        attendance = self.cleaned_data['attendance']
        # lesson = get_object_or_404(Course, id=lesson_id)
        # student = get_object_or_404(Student, id=student_id)
        obj = StudentInLesson.objects.get(lesson__id=lesson_id, student__id=student_id)
        obj.attendance = attendance
        obj.save()
        return obj
