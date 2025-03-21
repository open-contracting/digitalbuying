from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Sponsor


@modeladmin_register
class SponsorsAdmin(ModelAdmin):
    """Sponsors admin."""

    model = Sponsor
    menu_label = "Sponsor Logos"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("language",)
    list_filter = ("language",)
