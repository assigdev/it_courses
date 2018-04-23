from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def is_url_active(context, url):
    if url == context['request'].path:
        return 'active'
    return ''


@register.simple_tag(takes_context=True)
def is_base_url_active(context, path):
    header_path = context.get('header_path', False)
    if header_path and path == header_path:
        return 'active'
    return ''
