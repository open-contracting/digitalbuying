import urllib.parse

from django import template
from django.utils.translation import get_language
from wagtail.models import Page

from guidelines.models import GuidelinesListingPage
from navigation.models import FooterMenu, MainMenu

MINIMUM_DEPTH = 2

register = template.Library()


@register.simple_tag()
def page_translations(page):
    """Live translations of a page in other locales (for the language switcher)."""
    if page is None:
        return Page.objects.none()
    return page.get_translations().live()


# Retrieves the ancestors of the current page,
# filtering out the root (the per-language home is the first breadcrumb)
@register.inclusion_tag("includes/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth < MINIMUM_DEPTH:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gte=MINIMUM_DEPTH)
    parent = get_parent(ancestors, self.depth)
    return {
        "ancestors": ancestors,
        "parent": parent,
        "request": context["request"],
    }


def get_parent(ancestors, child_depth):
    """Get the parent based on the depth of the current item."""
    for item in ancestors:
        if item.depth == (child_depth - 1):
            return item
    return None


@register.simple_tag()
def main_menu(language):
    mainmenu = MainMenu.objects.filter(language=language).first()
    if mainmenu:
        return mainmenu
    # Default to en if not set for the other countries
    return MainMenu.objects.filter(language="en").first()


@register.simple_tag(takes_context=True)
def is_main_menu_link_active(context, link):
    request = context.get("request")
    if request:
        return urllib.parse.unquote(link) in request.path
    return False


@register.simple_tag()
def get_footer_content():
    language = get_language()
    guildelines = GuidelinesListingPage.objects.filter(locale__language_code=language).live()
    footer_content = FooterMenu.objects.filter(language=language).first()
    return {
        "guildelines": guildelines,
        "footer_content": footer_content,
    }
