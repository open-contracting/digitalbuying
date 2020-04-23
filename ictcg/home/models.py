from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtailtrans.models import TranslatablePage
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from ictcg.sponsors.models import Sponsor

class HomePage(TranslatablePage):
  """
  A TranslatablePage class for the homepage - WIP
  """

  body = RichTextField(blank=True, default="")

  content_panels = Page.content_panels + [
    FieldPanel('body'),
  ]

  search_fields = Page.search_fields + [
    index.SearchField('body'),
  ]