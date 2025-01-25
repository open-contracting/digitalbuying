from django import template

from case_studies.models import CaseStudyPage

register = template.Library()


@register.simple_tag()
def get_latest_case_studies(language):
    # Find the first 3 case studies based on their publication date (newest first)
    return CaseStudyPage.objects.filter(language__code=language).order_by("-publication_date").live()[:3]
