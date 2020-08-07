from django import template
from django.conf import settings
from wagtail.core.models import Page

register = template.Library()

@register.simple_tag(takes_context = True)
def get_cookie_notice(context):
    request = context.get('request')
    if request is None:
        return True
    return request.COOKIES.get('cookie_notice')

@register.simple_tag(takes_context = True)
def get_analytics_cookie(context):
    request = context.get('request')
    if request is None:
        return False
    return request.COOKIES.get('analytics', 'false') == 'true'

@register.simple_tag()
def get_analytics_id():
    return settings.ANALYTICS_ID 
