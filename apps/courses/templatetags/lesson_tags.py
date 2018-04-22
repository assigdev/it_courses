from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def get_student_in_lesson(context, lesson):
    user = context['request'].user
    return lesson.get_student_in_lesson(user.student)
