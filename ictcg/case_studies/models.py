from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtailtrans.models import TranslatablePage
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from ictcg.streams import blocks

class CaseStudiesListingPage(TranslatablePage):
    """
    A TranslatablePage class used for the entry to the case studies section of the site. 
    The page contains a list of the child (CaseStudyPage)
    """

    parent_page_types = ["base.HomePage"]
    subpage_types = ["case_studies.CaseStudyPage"]

    def get_context(self, request, *args, **kwards):
        context = super().get_context(request, *args, **kwards)
        featured_case_studies = CaseStudyPage.objects.filter(language__code=request.LANGUAGE_CODE).order_by('-publication_date').live().first()
        context['featured_case_studies'] = featured_case_studies
        if featured_case_studies:
            context['case_studies']  = CaseStudyPage.objects.filter(language__code=request.LANGUAGE_CODE).exclude(pk=featured_case_studies.pk).order_by('-publication_date').live()
        return context

class CaseStudyGuidelinesSectionTag(TaggedItemBase):
    content_object = ParentalKey('CaseStudyPage', on_delete=models.CASCADE, related_name='case_study_section_items')

class CaseStudyPage(TranslatablePage):
    """
    A TranslatablePage class used for case studies pages. 
    """

    parent_page_types = ["case_studies.CaseStudiesListingPage"]
    subpage_types = []

    introduction = models.CharField(max_length=240)

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
        help_text=_("Image dimensions should be 1912px wide × 714px high")
    )

    header_image_description = models.CharField(max_length=240)

    publication_date = models.DateField()

    collaborator = models.CharField(max_length=120)

    read_time = models.IntegerField(
        help_text=_("Time taken (in minutes) to read the case study")
    )

    section_tags = ClusterTaggableManager(through=CaseStudyGuidelinesSectionTag, blank=True)

    body = StreamField([
        ("rich_text_section", blocks.RichTextWithTitleBlock()),
        ("quote_section", blocks.QuoteBlock()),
    ], null=True, blank=True)

    content_panels = TranslatablePage.content_panels + [
        ImageChooserPanel("header_image"),
        FieldPanel('header_image_description'),
        FieldPanel('publication_date'),
        FieldPanel('read_time'),
        FieldPanel('collaborator'),
        FieldPanel('section_tags'),
        FieldPanel('introduction'),
        StreamFieldPanel("body"),
    ]

    search_fields = TranslatablePage.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    def get_context(self, request, *args, **kwards):
        context = super().get_context(request, *args, **kwards)
        siblings = CaseStudyPage.objects.filter(language__code=request.LANGUAGE_CODE).order_by('-publication_date').live()
        case_study_list = list(siblings.values_list('pk', flat=True))
        
        if self.pk in case_study_list:
            current_idx = case_study_list.index(self.pk)

            case_study_length = len(case_study_list) - 1 # 0 based index

            if current_idx + 1 <= case_study_length:
                context['next_page'] = siblings[current_idx + 1]

            if current_idx - 1 >= 0:
                context['prev_page'] = siblings[current_idx - 1]
       
        return context
