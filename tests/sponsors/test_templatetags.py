

from django.test import TestCase
from ictcg.sponsors.templatetags.sponsors_tags import get_footer_sponsors
from wagtail.images.models import Image


class TemplateTagsCaseStudiesTests(TestCase):
    fixtures = ['sponsors.json']

    def test_get_footer_sponsors(self):
        # Get footer sponsors based on the selected language from fixture data
        footer_sponsors = get_footer_sponsors('en')
        self.assertEqual(len(footer_sponsors), 2)
    
    def test_get_footer_sponsors_when_language_is_not_set(self):
        footer_sponsors = get_footer_sponsors('de')
        self.assertEqual(footer_sponsors, None)


