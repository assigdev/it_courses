from django import template
from apps.courses.models import CourseStudent
from django.template.defaultfilters import safe
from django.shortcuts import reverse
from apps.courses import tags_data

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_badge(context, course):
    user = context['request'].user
    if not user.is_authenticated or not user.is_student:
        return ''
    try:
        obj = CourseStudent.objects.get(course=course, student=user.student)
        if not obj.status:
            return ''
        return safe(tags_data.BADGE % obj.get_marker())
    except CourseStudent.DoesNotExist:
        return ''


@register.simple_tag(takes_context=True)
def get_status_options(context):
    user = context['request'].user
    course = context['course']
    obj = CourseStudent.objects.get(course=course, student=user.student)
    return safe(obj.get_status_options())


@register.simple_tag(takes_context=True)
def get_course_button(context, course):
    user = context['request'].user
    try:
        obj = CourseStudent.objects.get(course=course, student=user.student)
        return safe('<p class="text-center">%s</p>' % obj.get_status_display())
    except (CourseStudent.DoesNotExist, AttributeError):
        return safe(tags_data.COURSE_DETAIL % reverse('courses:detail', kwargs={'slug': course.slug}))


@register.simple_tag(takes_context=True)
def get_course_detail_button(context):
    user = context['request'].user
    course = context['course']
    if not user.is_authenticated:
        return safe(tags_data.USER_NOT_AUTH % reverse('accounts:login'))
    if not user.email_confirmed:
        return safe('<p>Подтвердите почту для доступа к курсу.</p>')
    if not user.is_student:
        return safe(tags_data.USER_NOT_STUD % (reverse('courses:users:create_student'), course.id))
    try:
        obj = CourseStudent.objects.get(course=course, student=user.student)
        if obj.status == 'in_view':
            return safe(tags_data.USER_ENROLL)
        # if obj.status in ['active', 'fail', 'fail_test', 'fail_view', 'finish']:
        return safe('<p>%s</p>' % obj.status)
    except CourseStudent.DoesNotExist:
        return safe(tags_data.USER_NOT_ENROLL % reverse('courses:enroll', kwargs={'slug': course.slug}))

