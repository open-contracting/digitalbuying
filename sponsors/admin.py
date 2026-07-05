from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Sponsor


class SponsorsViewSet(SnippetViewSet):
    """Sponsors admin."""

    model = Sponsor
    menu_label = "Sponsor Logos"
    icon = "placeholder"
    menu_order = 290
    add_to_admin_menu = True
    list_display = ("language",)
    list_filter = ("language",)


register_snippet(SponsorsViewSet)
