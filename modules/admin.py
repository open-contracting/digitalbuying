from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import LinksModule, MoreInformationModule


class MoreInformationModuleViewSet(SnippetViewSet):
    """More Information Module admin."""

    model = MoreInformationModule
    menu_label = "More information module"
    icon = "doc-full"
    list_display = (
        "language",
        "admin_title",
    )
    list_filter = ("language",)


class LinksModuleViewSet(SnippetViewSet):
    """Links module admin."""

    model = LinksModule
    menu_label = "Links module"
    icon = "doc-full"
    list_display = (
        "language",
        "admin_title",
    )
    list_filter = ("language",)


class ModulesGroup(SnippetViewSetGroup):
    menu_label = "Modules"
    menu_icon = "form"
    menu_order = 300
    add_to_admin_menu = True
    items = (MoreInformationModuleViewSet, LinksModuleViewSet)


register_snippet(ModulesGroup)
