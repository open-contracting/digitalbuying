from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtailtrans.models import TranslatablePage
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from ictcg.streams import blocks

class HomePage(TranslatablePage):
    """
    Homepage class
    """

    parent_page_types = ["wagtailtrans.TranslatableSiteRootPage"]
    subpage_types = ["guidelines.GuidelinesListingPage"]

    masthead_title = models.CharField(
        max_length=240,
        null=True,
        help_text=_("Title for masthead component")
    )

    masthead_description = RichTextField(blank=True, default="")

    masthead_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    masthead_link_title = models.CharField(
        max_length=240,
        null=True,
        blank=True,
        help_text=_("Title for link")
    )

    masthead_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    body = StreamField([
        ("content_section", blocks.RichTextWithTitleBlock()),
    ], null=True, blank=True)

    content_panels = TranslatablePage.content_panels + [
        StreamFieldPanel("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("masthead_title"),
                FieldPanel("masthead_description"),
                PageChooserPanel("masthead_link"),
                FieldPanel("masthead_link_title"),
                ImageChooserPanel("masthead_image"),
            ],
            heading=_('Masthead'),
        ),
        StreamFieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('masthead_title'),
        index.SearchField('masthead_description'),
        index.SearchField('body'),
    ]
