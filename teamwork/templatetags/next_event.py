from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def next_event(eventsSortedByDate):
    today = timezone.now()

    for event in eventsSortedByDate:
        if today <= event.date:
            return event
