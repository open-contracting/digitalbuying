from django import template
from ..models import Sponsor

register = template.Library()

@register.simple_tag(takes_context=True)
def get_sponsors(context):
  try:
    request = context['request']
    sponsors =  Sponsor.objects.filter(language=request.LANGUAGE_CODE).first()
    if sponsors:
      return sponsors
    else:
      # Default to en if not set for the other countries
      return Sponsor.objects.filter(language='en').first()
  except Sponsor.DoesNotExist:
    return Sponsor.objects.none()
