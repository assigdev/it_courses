from django import template
register = template.Library()


@register.filter(name='add_class')
def add_class(field, class_name):
    return field.as_widget(attrs={"class": class_name})


@register.filter(name='add_checked')
def add_checked(field, is_checked):
    if is_checked:
        return field.as_widget(attrs={'checked': 'checked', "class": 'js-ajax-send'})
    return field.as_widget(attrs={"class": 'js-ajax-send'})


@register.filter(name='add_link_value')
def add_link_value(field, value):
    return field.as_widget(attrs={"value": value})
