from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from django.utils.translation import ugettext_lazy as _
from .models import MainMenu

class MainMenuAdmin(ModelAdmin):
  """Main menu admin."""

  model = MainMenu
  menu_label = _("Main menu")
  menu_icon = "list-ul"
  menu_order = 200
  add_to_settings_menu = False
  exclude_from_explorer = False

@modeladmin_register
class MenusGroup(ModelAdminGroup):
  menu_label = _("Menus")
  menu_icon = "form"
  menu_order = 300 
  items = (MainMenuAdmin,)
