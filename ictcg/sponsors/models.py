import logging

from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailtrans.models import TranslatablePage

from ictcg.streams import blocks


class Sponsor(ClusterableModel):
    language = models.CharField(max_length=100, choices=settings.LANGUAGES)

    panels = [
        FieldPanel("language"),
        InlinePanel("sponsor_items", label="Sponsor Item"),
    ]

    def __str__(self):
        return f"Sponsors - {self.language}"

    def save(self, *args, **kwards):
        try:
            clear_sponsors_footer_cache(self.language)
        except Exception:
            logging.exception("Error deleting sponsors cache")
        return super().save(*args, **kwards)


class SponsorItem(Orderable):
    name = models.CharField(max_length=140, blank=True, help_text="Title")

    url = models.URLField(blank=True, help_text="URL for sponsor link")

    logo = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        help_text="Sponsor image or logo",
        on_delete=models.SET_NULL,
    )

    logo_description = models.CharField(max_length=240, null=True, help_text="Alt tag description for sponsor logo")

    show_in_footer = models.BooleanField(default=False, blank=True)

    show_on_homepage = models.BooleanField(default=False, blank=True)

    show_on_sponsorship = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
        ImageChooserPanel("logo"),
        FieldPanel("logo_description"),
        FieldPanel("show_in_footer"),
        FieldPanel("show_on_homepage"),
        FieldPanel("show_on_sponsorship"),
    ]

    sponsor = ParentalKey("Sponsor", related_name="sponsor_items", default="")


class SponsorsPage(TranslatablePage):
    """
    SponsorsPage page - allows for listing of site sponsors along with additional supporters and contributors
    Can be nested under the homepage or generic pages.
    """

    parent_page_types = ["base.HomePage", "base.GenericPageWithSubNav", "base.GenericPage"]
    subpage_types = ["base.GenericPageWithSubNav", "base.GenericPage"]

    body = StreamField(
        [
            ("rich_text_section", blocks.RichTextWithTitleBlock()),
            ("sponsors_section", blocks.RichTextWithTitleBlock(template="streams/sponsors_block.html")),
            ("supports_section", blocks.SupportersBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = [
        *TranslatablePage.content_panels,
        StreamFieldPanel("body"),
    ]

    search_fields = [
        *TranslatablePage.search_fields,
        index.SearchField("body"),
    ]


def clear_sponsors_footer_cache(language_code):
    sponsors_footer = make_template_fragment_key("sponsors_footer", [language_code])
    cache.delete_many([sponsors_footer])


@receiver(pre_delete, sender=Sponsor)
def on_footer_menu_delete(_sender, instance, **kwargs):
    """On Sponsor delete, clear the cache."""
    clear_sponsors_footer_cache(instance.language)
