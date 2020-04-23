from django import template
from wagtail.core.models import Page

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