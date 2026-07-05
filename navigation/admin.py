from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import FooterMenu, MainMenu


class MainMenuViewSet(SnippetViewSet):
    """Main menu admin."""

    model = MainMenu
    menu_label = "Main menu"
    icon = "list-ul"


class FooterMenuViewSet(SnippetViewSet):
    """Footer menu admin."""

    model = FooterMenu
    menu_label = "Footer menu"
    icon = "list-ul"


class MenusGroup(SnippetViewSetGroup):
    menu_label = "Menus"
    menu_icon = "form"
    menu_order = 300
    add_to_admin_menu = True
    items = (MainMenuViewSet, FooterMenuViewSet)


register_snippet(MenusGroup)
