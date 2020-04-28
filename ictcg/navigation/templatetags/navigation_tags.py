from django import template
from wagtail.core.models import Page
from ..models import MainMenu

register = template.Library()

# Retrieves the ancestors of the current page, 
# filtering out the top 3 levels (root, translation-root and home)
@register.inclusion_tag('tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
  self = context.get('self')
  if self is None or self.depth <= 3:
    ancestors = ()
  else:
    ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=3)
  return {
    'ancestors': ancestors,
    'request': context['request'],
  }

@register.simple_tag(takes_context=True)
def main_menu(context):
  try:
    request = context['request']
    mainmenu =  MainMenu.objects.filter(language=request.LANGUAGE_CODE).first()
    if mainmenu:
      return mainmenu
    else:
      # Default to en if not set for the other countries
      return MainMenu.objects.filter(language='en').first()
  except MainMenu.DoesNotExist:
    return MainMenu.objects.none()
  
@register.simple_tag(takes_context=True)
def is_main_menu_link_active(context, slug):
  request = context['request']
  return slug in request.path
  