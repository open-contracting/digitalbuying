from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import FooterMenu, MainMenu


class MainMenuAdmin(ModelAdmin):
    """Main menu admin."""

    model = MainMenu
    menu_label = "Main menu"
    menu_icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False


class FooterMenuAdmin(ModelAdmin):
    """Footer menu admin."""

    model = FooterMenu
    menu_label = "Footer menu"
    menu_icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False


@modeladmin_register
class MenusGroup(ModelAdminGroup):
    menu_label = "Menus"
    menu_icon = "form"
    menu_order = 300
    items = (MainMenuAdmin, FooterMenuAdmin)
