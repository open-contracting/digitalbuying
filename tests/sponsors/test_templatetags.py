from django.test import TestCase

from ictcg.sponsors.templatetags.sponsors_tags import (
    get_footer_sponsors,
    get_homepage_sponsors,
    get_sponsorship_page_sponsors,
)


class TemplateTagsCaseStudiesTests(TestCase):
    fixtures = ["sponsors.json"]

    def test_get_footer_sponsors(self):
        # Get footer sponsors based on the selected language from fixture data
        footer_sponsors = get_footer_sponsors("en")
        self.assertEqual(len(footer_sponsors), 2)

    def test_get_footer_sponsors_when_language_is_not_set(self):
        footer_sponsors = get_footer_sponsors("de")
        self.assertEqual(footer_sponsors, None)


class TemplateTagsHomePageTests(TestCase):
    fixtures = ["sponsors.json"]

    def test_get_homepage_sponsors(self):
        # Get homepage sponsors based on the selected language from fixture data
        homepage_sponsors = get_homepage_sponsors("en")
        self.assertEqual(len(homepage_sponsors), 2)

    def test_get_footer_sponsors_when_language_is_not_set(self):
        homepage_sponsors = get_homepage_sponsors("de")
        self.assertEqual(homepage_sponsors, None)


class TemplateTagsSponsorshipTests(TestCase):
    fixtures = ["sponsors.json"]

    def test_get_sponsorship_page_sponsors(self):
        # Get homepage sponsors based on the selected language from fixture data
        sponsorship_page_sponsors = get_sponsorship_page_sponsors("en")
        self.assertEqual(len(sponsorship_page_sponsors), 2)

    def test_get_sponsorship_page_sponsors_when_language_is_not_set(self):
        homepage_sponsors = get_sponsorship_page_sponsors("de")
        self.assertEqual(homepage_sponsors, None)
