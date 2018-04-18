from django import template
register = template.Library()


@register.filter(name='is_active')
def is_active(slug, active_slug):
    if slug == active_slug:
        return 'active'
