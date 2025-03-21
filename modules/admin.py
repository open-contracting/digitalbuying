from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import LinksModule, MoreInformationModule


class MoreInformationModuleAdmin(ModelAdmin):
    """More Information Module admin."""

    model = MoreInformationModule
    menu_label = "More information module"
    menu_icon = "doc-full"
    menu_order = 000
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "language",
        "admin_title",
    )
    list_filter = ("language",)


class LinksModuleAdmin(ModelAdmin):
    """Links module admin."""

    model = LinksModule
    menu_label = "Links module"
    menu_icon = "doc-full"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "language",
        "admin_title",
    )
    list_filter = ("language",)


@modeladmin_register
class ModulesGroup(ModelAdminGroup):
    menu_label = "Modules"
    menu_icon = "form"
    menu_order = 300
    items = (MoreInformationModuleAdmin, LinksModuleAdmin)
