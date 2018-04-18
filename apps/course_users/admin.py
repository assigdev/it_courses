from django.contrib import admin
from .models import Student, Teacher


def user_full_name(obj):
    return obj.user.get_full_name()
user_full_name.short_description = 'Название статьи'
user_full_name.allow_tags = True


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (user_full_name, 'social_status', 'school', 'parent_phone')
    list_filter = ('social_status',)


admin.site.register(Teacher)
