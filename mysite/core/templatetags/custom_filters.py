from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def reading_time(value):
    return f"~{round(len(value.split(' ')) * 0.5)} мин"


@register.simple_tag
def add_per():
    site_status = "Работает штатно"
    return site_status
