from django import forms

from apps.courses.models import StudentInLesson


class HomeworkLinkForm(forms.Form):
    lesson_id = forms.IntegerField(required=True)
    student_id = forms.IntegerField(required=True)
    link = forms.URLField(required=False)

    def save(self):
        lesson_id = self.cleaned_data['lesson_id']
        student_id = self.cleaned_data['student_id']
        link = self.cleaned_data['link']
        obj = StudentInLesson.objects.get(lesson__id=lesson_id, student__id=student_id)
        obj.homework_link = link
        obj.save()
        return obj
