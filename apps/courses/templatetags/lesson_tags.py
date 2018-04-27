from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def get_student_in_lesson(context, lesson, student):
    if lesson is None:
        return ''
    return lesson.get_student_in_lesson(student)
