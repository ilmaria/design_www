from django import template
from urllib.parse import quote_plus

register = template.Library()

@register.filter
def urlencode_plus(value):
    return quote_plus(value)

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{}h {}min'.format(hours, minutes)
