from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from django.conf import settings

class Sponsor(ClusterableModel):
    language = models.CharField(
        max_length=100,
        choices=settings.LANGUAGES
    )
    title = models.CharField(max_length=100)
    introduction = RichTextField(blank=True)

    panels = [
        FieldPanel("language"),
        FieldPanel("title"),
        FieldPanel("introduction"),
        InlinePanel("sponsor_items", label="Sponsor Item")
    ]

    def __str__(self):
        return self.title

class SponsorItem(Orderable):

    name = models.CharField(
        max_length=140,
        blank=True,
        help_text='Title'
    )

    url = models.URLField(blank=True, help_text=_("URL for sponsor link"))

    logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text=_('Sponsor image or logo'),
        on_delete=models.SET_NULL,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
        ImageChooserPanel("logo")
    ]

    sponsor = ParentalKey("Sponsor", related_name="sponsor_items", default='')
