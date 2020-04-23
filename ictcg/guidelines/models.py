from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from wagtailtrans.models import TranslatablePage, Language
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable, Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import (
  FieldPanel,
  MultiFieldPanel,
  StreamFieldPanel, 
  InlinePanel,
  ObjectList,
  TabbedInterface,
  PageChooserPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from ictcg.guidelines.choices import COLOUR_CHOICES
from ictcg.guidelines.utils import hex_to_rgb
from ictcg.streams import blocks

class GuidelinesListingPage(TranslatablePage):
  """
  A TranslatablePage class used for the entry to the guidelines section of the site. 
  The page contains a list of the child (GuidelinesSectionPage)
  """

  parent_page_types = ["home.HomePage"]
  subpage_types = ["guidelines.GuidelinesSectionPage"]
  max_count = 1

  introduction = RichTextField(blank=True, default="")

  search_fields = Page.search_fields + [
    index.SearchField('introduction'),
  ]

  content_panels = Page.content_panels + [
    FieldPanel('introduction'),
  ]

  def get_context(self, request, *args, **kwards):
    context = super().get_context(request, *args, **kwards)
    context['descendants'] = Page.objects.child_of(self).live()
    return context
    

class GuidelinesSectionPage(TranslatablePage):
  """
  A TranslatablePage class used for each subsection with the guidelines section.
  """
  
  parent_page_types = ["guidelines.GuidelinesListingPage"]
  subpage_types = ["guidelines.GuidancePage"]

  subtitle = models.CharField(
    max_length=140, 
    blank=False
  )

  section_colour = models.CharField(
    max_length=140, 
    choices=COLOUR_CHOICES, 
    null=False, 
    blank=False
  )

  landing_page_summary = models.CharField(
    max_length=240,
    null=True,
    blank=False,
    help_text=_("Text to be shown on the guidelines landing page")
  )
  
  body = StreamField([
    ("content", blocks.RichTextWithTitleBlock()),
  ], null=True, blank=True)

  sub_sections_title = models.CharField(
    max_length=140, 
    blank=False,
    help_text=_("Title for child pages under this section")
  )

  content_panels = Page.content_panels + [
    FieldPanel("subtitle"),
    FieldPanel("section_colour"),
    StreamFieldPanel("body"),
    FieldPanel("sub_sections_title"),
    FieldPanel("landing_page_summary"),
  ]

  search_fields = Page.search_fields + [
    index.SearchField('body'),
  ]

  def get_context(self, request, *args, **kwards):
    context = super().get_context(request, *args, **kwards)
    guidelines = self.get_parent()
    context['guidelines_title'] = guidelines.title
    return context

# TODO: Hide snippets for other languages
# class CustomizedChooserPanel(SnippetChooserPanel):
#   def on_form_bound(self):
#     page_language = self.form.initial['language']
#     language_code = Language.objects.get(id=page_language)
#     choices = MoreInformationModule.objects.filter(language=language_code.code)
#     self.form.fields["more_information_module"].queryset = choices
#     super().on_form_bound()

class GuidancePage(TranslatablePage):
  """
  A TranslatablePage class used for the many content pages for each guidelines subsection
  """

  parent_page_types = ["guidelines.GuidelinesSectionPage"]
  subpage_types = []

  body = StreamField([
    ("content_section", blocks.RichTextWithTitleBlock()),
    ("dos_and_donts", blocks.DosAndDontsBlock()),
  ], null=True, blank=True)

  content_panels = TranslatablePage.content_panels + [
    StreamFieldPanel("body"),
  ]

  more_information_module = models.ForeignKey(
    'modules.MoreInformationModule',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+'
  )

  links_module = models.ForeignKey(
    'modules.LinksModule',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+'
  )

  Sidebar_panels = [
    SnippetChooserPanel("more_information_module"),
    SnippetChooserPanel("links_module")
  ]

  edit_handler = TabbedInterface([
    ObjectList(content_panels, heading='Content'),
    ObjectList(Sidebar_panels, heading='Sidebar'),
    ObjectList(TranslatablePage.settings_panels, heading='Settings'),
    ObjectList(TranslatablePage.promote_panels, heading='Promote')
  ])

  search_fields = Page.search_fields + [
    index.SearchField('body'),
  ]

  def get_context(self, request, *args, **kwards):
    context = super().get_context(request, *args, **kwards)
    context['prev_sibling'] = self.get_prev_siblings().live().first()
    context['next_sibling'] = self.get_next_siblings().live().first()
    guidelines =  GuidelinesListingPage.objects.ancestor_of(self).live().first()
    section = GuidelinesSectionPage.objects.ancestor_of(self).live().first()
    context['section'] = section
    context['section_colour_rgb'] = ','.join(str(v) for v in hex_to_rgb(section.section_colour))
    context['guidelines_title'] = guidelines.title
    return context
  