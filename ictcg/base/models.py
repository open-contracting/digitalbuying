from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailtrans.models import TranslatablePage

from ictcg.streams import blocks


class HomePage(TranslatablePage):
    """Homepage class."""

    parent_page_types = ["wagtailtrans.TranslatableSiteRootPage"]
    subpage_types = [
        "guidelines.GuidelinesListingPage",
        "base.GenericPageWithSubNav",
        "case_studies.CaseStudiesListingPage",
        "base.GenericPage",
        "sponsors.SponsorsPage",
    ]

    masthead_title = models.CharField(max_length=240, null=True, help_text="Title for masthead component")

    masthead_description = RichTextField(blank=True, default="")

    masthead_link = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.SET_NULL
    )

    masthead_link_title = models.CharField(max_length=240, null=True, blank=True, help_text="Title for link")

    masthead_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    masthead_image_description = models.CharField(
        max_length=240, null=True, blank=True, help_text="Alt tag description for image"
    )

    body = StreamField(
        [
            ("rich_text_section", blocks.HomePageRichTextBlock()),
            ("highlight_list_section", blocks.HighlightListBlock()),
            ("case_study_section", blocks.CaseStudyBlock()),
            ("sponsors_section", blocks.HomePageRichTextBlock(template="streams/homepage_sponsors_block.html")),
        ],
        null=True,
        blank=True,
    )

    content_panels = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel("masthead_title"),
                FieldPanel("masthead_description"),
                PageChooserPanel("masthead_link"),
                FieldPanel("masthead_link_title"),
                ImageChooserPanel("masthead_image"),
                FieldPanel("masthead_image_description"),
            ],
            heading="Masthead",
        ),
        StreamFieldPanel("body"),
    ]

    search_fields = [
        *Page.search_fields,
        index.SearchField("masthead_title"),
        index.SearchField("masthead_description"),
        index.SearchField("body"),
    ]

    def clean(self):
        super().clean()
        if self.masthead_image and not self.masthead_image_description:
            raise ValidationError(
                {
                    "masthead_image_description": "Please enter description for the masthead image",
                }
            )


class GenericPageWithSubNav(TranslatablePage):
    """
    Generic page class which allows rich text and quote components to be added.  Can only be added under the homepage but can be nested itself.
    Page includes a sub navigation on the left of the layout for quick links to content on the page. This is auto genereated based on the body components.
    """

    parent_page_types = ["base.HomePage", "base.GenericPageWithSubNav", "base.GenericPage"]
    subpage_types = ["base.GenericPageWithSubNav", "base.GenericPage", "sponsors.SponsorsPage"]

    navigation_title = models.CharField(max_length=120, null=True, blank=True, help_text="Title for Navigation")

    body = StreamField(
        [
            ("rich_text_section", blocks.RichTextWithTitleBlock()),
            ("quote_section", blocks.QuoteBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = [
        *TranslatablePage.content_panels,
        FieldPanel("navigation_title"),
        StreamFieldPanel("body"),
    ]


class GenericPage(TranslatablePage):
    """
    Generic page class which allows rich text and quote components to be added.
    Similar page to GenericPageWithSubNav but does not include the sub-navigation component.
    """

    parent_page_types = ["base.HomePage", "base.GenericPageWithSubNav", "base.GenericPage"]
    subpage_types = ["base.GenericPageWithSubNav", "base.GenericPage", "sponsors.SponsorsPage"]

    introduction = RichTextField(blank=True, default="")

    body = StreamField(
        [
            ("rich_text_section", blocks.RichTextWithTitleBlock()),
            ("quote_section", blocks.QuoteBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = [
        *TranslatablePage.content_panels,
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]
