from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

class MainMenu(ClusterableModel):
  """
  MainMenu class for header links. Contains Orderable MenuItem class.
  """

  admin_title = models.CharField(
    max_length=100, 
    blank=False,
    null=True
  )

  title = models.CharField(max_length=100)

  language = models.CharField(
    max_length=100, 
    choices=settings.LANGUAGES
  )

  logo = models.ForeignKey(
    'wagtailimages.Image',
    blank=False,
    null=True,
    related_name='+',
    on_delete=models.SET_NULL,
  )

  button_text = models.CharField(
    max_length=100, 
    blank=False,
    null=False,
    default="Menu"
  )

  button_aria_label = models.CharField(
    max_length=100, 
    default="Show or hide Top Level Navigation",
    help_text=_('Description for navigation button aria label'),
  )

  navigation_aria_label = models.CharField(
    max_length=100,
    default="Top Level Navigation",
    help_text=_('Description for navigation aria label'),
  )

  panels = [
    FieldPanel("title"),
    FieldPanel("language"),
    ImageChooserPanel("logo"),
    FieldPanel("button_text"),
    FieldPanel("button_aria_label"),
    FieldPanel("navigation_aria_label"),
    InlinePanel("menu_items", label="Menu Item")
  ]

  def __str__(self):
    return f"{self.title} - {self.language}"

class MenuItem(Orderable):
  """
  Orderable class for link data
  """

  title = models.CharField(max_length=100, blank=True)
  url = models.CharField(max_length=500, blank=True)
  page = models.ForeignKey(
    'wagtailcore.Page',
    null=True,
    blank=True,
    related_name="+",
    on_delete=models.CASCADE
  )
  open_in_new_tab = models.BooleanField(default=False, blank=True)

  panels = [
    FieldPanel("title"),
    FieldPanel("url"),
    PageChooserPanel("page"),
    FieldPanel("open_in_new_tab"),
  ]

  menu = ParentalKey("MainMenu", related_name="menu_items")

  @property
  def link(self):
    if self.page:
      return self.page.url
    elif self.url:
      return self.url
    return "#"