from django.db import models
from django.conf import settings
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
)

class KeyModuleFields(models.Model):
    """
    Reuseable class for generic module data
    """

    class Meta:
        abstract = True

    language = models.CharField(
        max_length=100,
        choices=settings.LANGUAGES
    )

    admin_title = models.CharField(
        max_length=140,
        blank=False,
        null=True,
        help_text='Title to appear in the admin area'
    )

    title = models.CharField(
        max_length=140,
        blank=False,
        null=True,
    )

    panels = [
        FieldPanel("language"),
        FieldPanel("admin_title"),
        FieldPanel("title"),
    ]


class Links(models.Model):
    """
    Reuseable class for link data
    """

    class Meta:
        abstract = True

    link_text = models.CharField(
        max_length=140,
        blank=True,
        help_text='Text for link'
    )

    url = models.URLField(null=True, blank=True)

    open_in_new_tab = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("link_text"),
        FieldPanel('url'),
        FieldPanel("open_in_new_tab"),
    ]

@register_snippet
class MoreInformationModule(KeyModuleFields):
    """
     A class that extends KeyModuleFields class that is displayed as a snippet within the admin area.
     This is used as a foreignField in the GuidancePage class
    """

    description = RichTextField(blank=True, default="")

    panels = KeyModuleFields.panels + [
        FieldPanel("description"),
    ]

    def __str__(self):
        return f"{self.admin_title} - {self.language}"

class OrderableLinks(Orderable, Links):
    """
     A class that extends Orderable and Links classes.
     Extending Orderable allow for links to be arranaged in the order choosen by the user
    """
    panels = Links.panels + []
    links = ParentalKey(
        "LinksModule", related_name="orderable_links", default='')


@register_snippet
class LinksModule(ClusterableModel, KeyModuleFields):
    """
     A class that extends ClusterableModel and KeyModuleFields classes that is displayed as a snippet within the admin area.
     This is used as a foreignField in the GuidancePage class.
    """
    panels = KeyModuleFields.panels + [
        InlinePanel("orderable_links", label="Links")
    ]

    def __str__(self):
        return f"{self.admin_title} - {self.language}"
