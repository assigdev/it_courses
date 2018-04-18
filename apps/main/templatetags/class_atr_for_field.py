from django import template
register = template.Library()


@register.filter(name='add_class')
def add_class(field, class_name):
    # if field.field.required:
    #     return field.as_widget(attrs={"class": class_name, 'placeholder': '*Обязательное поле'})
    return field.as_widget(attrs={"class": class_name})
