from django.test import TestCase
from unittest.mock import Mock, patch

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from wagtailtrans.models import TranslatablePage

from ictcg.guidelines.models import GuidelinesListingPage, GuidelinesSectionPage, GuidancePage
from ictcg.base.models import HomePage


class GuidelinesListingPageTests(WagtailPageTests):
    def test_listing_page_can_be_created_under_homepage(self):
        # You can create a GuidelinesListingPage under an HomePage
        self.assertCanCreateAt(HomePage, GuidelinesListingPage)

    def test_section_page_can_be_created_under_listing_page(self):
        # You can create a GuidelinesSectionPage under an GuidelinesListingPage
        self.assertCanCreateAt(GuidelinesListingPage, GuidelinesSectionPage)

    def test_guidance_page_cant_be_created_under_listing_page(self):
        # You can not create a GuidancePage under an GuidelinesListingPage
        self.assertCanNotCreateAt(GuidelinesListingPage, GuidancePage)

    def test_listing_page_inherits_from_translatable_page_class(self):
        assert issubclass(GuidelinesListingPage, TranslatablePage)


class GuidelinesSectionPageTests(WagtailPageTests):
    fixtures = ["app.json"]

    def test_section_page_can_only_be_created_under_list_page(self):
        # An GuidelinesSectionPage can only be created under an GuidelinesListingPage
        self.assertAllowedParentPageTypes(GuidelinesSectionPage, {GuidelinesListingPage})

    def test_guidance_page_can_be_created_under_sectiong_page(self):
        # An GuidancePage can be created inder an GuidelinesListingPage
        self.assertCanCreateAt(GuidelinesSectionPage, GuidancePage)

    def test_section_page_inherits_from_translatable_page_class(self):
        assert issubclass(GuidelinesListingPage, TranslatablePage)

    @patch("ictcg.guidelines.models.GuidelinesSectionPage.clear_from_caches")
    def test_clear_cache_is_called_on_save(self, clear_from_caches):
        # When save is called on a GuidelinesSectionPage class clear_guidelines_listing_cache should be called
        GuidelinesSectionPage.objects.create(
            path="00010002000100010003",
            depth="5",
            landing_page_summary="Summary",
            subtitle="Overview",
            section_colour="primary-1",
            title="Test section page",
        )

        self.assertTrue(clear_from_caches.called)
        self.assertEqual(clear_from_caches.call_count, 1)

    def test_section_page_should_include_pagination_link_to_first_child_page(self):
        response = self.client.get("/en/guidelines/prepare-and-plan/")
        self.assertContains(
            response,
            '<a class="ictcg-pagination__link ictcg-pagination__link--next" href="/en/guidelines/prepare-and-plan/form-a-team/">',
            status_code=200,
        )


class GuidancePageTests(WagtailPageTests):
    fixtures = ["app.json"]

    def test_guidance_page_can_only_be_created_under_section_page(self):
        # An GuidelinesSectionPage can only be created under an GuidelinesListingPage
        self.assertAllowedParentPageTypes(GuidancePage, {GuidelinesSectionPage})

    def test_guidance_page_inherits_from_translatable_page_class(self):
        assert issubclass(GuidelinesListingPage, TranslatablePage)

    def test_guidance_page_pagination_links_first_page_in_section(self):
        # Ensure the data for the pagation links is correct
        # As this is the first page in the section it should get the parents as the prev link
        # Based on fixture data
        # Page ID should be 9
        # Prev page will be 7
        # next page will be 10
        response = self.client.get("/en/guidelines/prepare-and-plan/form-a-team/")

        self.assertTrue("prev_page" in response.context)
        self.assertTrue("next_page" in response.context)
        self.assertEqual(response.context["prev_page"].pk, 7)
        self.assertEqual(response.context["next_page"].pk, 10)

    def test_guidance_page_pagination_links_last_page_in_section(self):
        # Ensure the data for the pagation links is correct
        # As this is the last page in the section it should get it's parents next sibling as the next page link
        # Based on fixture data
        # Page ID should be 10
        # Prev page will be 9
        # next page will be 8
        response = self.client.get("/en/guidelines/prepare-and-plan/user-needs/")

        self.assertTrue("prev_page" in response.context)
        self.assertTrue("next_page" in response.context)
        self.assertEqual(response.context["prev_page"].pk, 9)
        self.assertEqual(response.context["next_page"].pk, 8)

    @patch("ictcg.guidelines.models.GuidancePage.clear_from_caches")
    def test_clear_cache_is_called_on_save(self, clear_from_caches):
        GuidancePage.objects.create(path="000100020001000100010003", depth="6", title="Test guidance page")

        self.assertTrue(clear_from_caches.called)
        self.assertEqual(clear_from_caches.call_count, 1)


class OnDeletePageSignalsTest(TestCase):
    fixtures = ["app.json"]

    @patch("ictcg.guidelines.models.GuidancePage.clear_from_caches")
    def test_cache_is_cleared_on_guidelines_section_page_delete(self, clear_from_caches):
        # When delete is called on a GuidelinesSectionPage class clear_guidelines_section_cache should be called and
        # clear_guidelines_listing_cache should not be called

        # Create a section page which has no children so we can test delete function without triggering other events based on the tree structure
        # ie, a child page also being deleted when the parent is removed
        guidelines_section_page = GuidelinesSectionPage.objects.create(
            path="00010002000100010003",
            depth="5",
            landing_page_summary="Summary",
            subtitle="Overview",
            section_colour="primary-1",
            title="Test section page",
        )
        guidelines_section_page.delete()

        self.assertFalse(clear_from_caches.called)

    @patch("ictcg.guidelines.models.GuidancePage.clear_from_caches")
    def test_cache_is_cleared_on_guidance_page_delete(self, clear_from_caches):
        # When delete is called on a GuidancePage class clear_guidelines_section_cache and
        # clear_guidelines_listing_cache should both be called
        guidance_page = GuidancePage.objects.get(pk=9)
        guidance_page.delete()

        self.assertTrue(clear_from_caches.called)
