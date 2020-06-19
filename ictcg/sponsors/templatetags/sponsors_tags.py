from django import template
from ictcg.sponsors.models import SponsorItem

register = template.Library()

@register.simple_tag()
def get_footer_sponsors(language):
    sponsors = SponsorItem.objects.filter(sponsor__language=language, show_in_footer=True)
    if sponsors:
        return sponsors
    else:
        return None

@register.simple_tag()
def get_homepage_sponsors(language):
    sponsors = SponsorItem.objects.filter(sponsor__language=language, show_on_homepage=True)
    if sponsors:
        return sponsors
    else:
        return None
