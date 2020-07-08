from django import template
from wagtail.core.models import Page

register = template.Library()

@register.simple_tag(takes_context = True)
def get_cookie_notice(context):
    request = context['request']
    return request.COOKIES.get('cookie_notice')

@register.simple_tag(takes_context = True)
def get_analytics_cookie(context):
    request = context['request']
    return request.COOKIES.get('analytics', 'false')