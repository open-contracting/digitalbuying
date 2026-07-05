from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
)
from wagtail.fields import RichTextField
from wagtail.models import Orderable


class KeyModuleFields(models.Model):
    """Reuseable class for generic module data."""

    language = models.CharField(max_length=100, choices=settings.LANGUAGES)

    admin_title = models.CharField(max_length=140, blank=False, help_text="Title to appear in the admin area")

    title = models.CharField(max_length=140, blank=False)

    panels = [
        FieldPanel("language"),
        FieldPanel("admin_title"),
        FieldPanel("title"),
    ]

    class Meta:
        abstract = True


class Links(models.Model):
    """Reuseable class for link data."""

    link_text = models.CharField(max_length=140, blank=True, help_text="Text for link")

    url = models.URLField(blank=True)

    open_in_new_tab = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("link_text"),
        FieldPanel("url"),
        FieldPanel("open_in_new_tab"),
    ]

    class Meta:
        abstract = True


class MoreInformationModule(KeyModuleFields):
    """
    A class that extends KeyModuleFields class that is displayed as a snippet within the admin area.
    This is used as a foreignField in the GuidancePage class.
    """

    description = RichTextField(blank=True, default="")

    panels = [
        *KeyModuleFields.panels,
        FieldPanel("description"),
    ]

    def __str__(self):
        return f"{self.admin_title} - {self.language}"


class OrderableLinks(Orderable, Links):
    """
    A class that extends Orderable and Links classes.
    Extending Orderable allow for links to be arranaged in the order choosen by the user.
    """

    panels = [
        *Links.panels,
    ]
    links = ParentalKey("LinksModule", related_name="orderable_links", default="")

    def __str__(self):
        return self.link_text


class LinksModule(ClusterableModel, KeyModuleFields):
    """
    A class that extends ClusterableModel and KeyModuleFields classes that is displayed as a snippet within the admin
    area. This is used as a foreignField in the GuidancePage class.
    """

    panels = [
        *KeyModuleFields.panels,
        InlinePanel("orderable_links", label="Links"),
    ]

    def __str__(self):
        return f"{self.admin_title} - {self.language}"
