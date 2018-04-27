from django import template
from apps.courses.models import CourseStudent
from django.template.defaultfilters import safe
from django.shortcuts import reverse
from apps.courses import tags_data

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_badge(context, course):
    user = context['request'].user
    if not user.is_authenticated or not user.is_student():
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
    course = context['course']
    student = context['student']
    obj = CourseStudent.objects.get(course=course, student=student)
    return safe(obj.get_status_options())


@register.simple_tag(takes_context=True)
def get_course_button(context, course):
    user = context['request'].user
    try:
        obj = CourseStudent.objects.get(course=course, student=user.student)
        if obj.status in ('active', 'finish'):
            return safe(tags_data.USER_ACTIVE_BUTTON % reverse('courses:lessons', kwargs={'slug': course.slug}))
        p_class = 'text-success' if obj.status == 'in_view' else 'text-danger'
        return safe('<p class="text-center %s">%s</p>' % (p_class, obj.get_status_display()))
    except (CourseStudent.DoesNotExist, AttributeError):
        return safe(tags_data.COURSE_DETAIL % reverse('courses:detail', kwargs={'slug': course.slug}))


@register.simple_tag(takes_context=True)
def get_course_detail_button(context):
    user = context['request'].user
    course = context['course']
    if not user.is_authenticated:
        return safe(tags_data.USER_NOT_AUTH % reverse('accounts:login'))
    if not user.email_confirmed:
        return safe('<h5 class="text-info">Подтвердите почту для доступа к курсу.</p>')
    if not user.is_student():
        return safe(tags_data.USER_NOT_STUD % (reverse('courses:users:create_student'), course.id))
    try:
        obj = CourseStudent.objects.get(course=course, student=user.student)
        if obj.status == 'in_view':
            return safe(tags_data.USER_ENROLL)
        if obj.status in ('active', 'finish'):
            return safe(tags_data.USER_ACTIVE % reverse('courses:lessons', kwargs={'slug': course.slug}))
        return safe('<h5 class="text-danger">%s</p>' % obj.get_status_display())
    except CourseStudent.DoesNotExist:
        return safe(tags_data.USER_NOT_ENROLL % reverse('courses:enroll', kwargs={'slug': course.slug}))

