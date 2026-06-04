from django import template
from datetime import datetime
from django.core.cache import cache
from django.template.loader import render_to_string

register = template.Library()
