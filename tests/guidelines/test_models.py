from django.test import TestCase
from unittest.mock import Mock, patch

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from wagtailtrans.models import TranslatablePage

from ictcg.guidelines.models import GuidelinesListingPage, GuidelinesSectionPage, GuidancePage
from ictcg.base.models import HomePage

# import pudb; pu.db()
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
    fixtures = ['app.json']

    def test_section_page_can_only_be_created_under_list_page(self):
        # An GuidelinesSectionPage can only be created under an GuidelinesListingPage
        self.assertAllowedParentPageTypes(GuidelinesSectionPage, {GuidelinesListingPage})

    def test_guidance_page_can_be_created_under_sectiong_page(self):
        # An GuidancePage can be created inder an GuidelinesListingPage
        self.assertCanCreateAt(GuidelinesSectionPage, GuidancePage)

    def test_section_page_inherits_from_translatable_page_class(self):
        assert issubclass(GuidelinesListingPage, TranslatablePage)

    @patch('ictcg.guidelines.models.clear_guidelines_listing_cache')
    def test_clear_cache_is_called_on_save(self, mock):
        # When save is called on a GuidelinesSectionPage class clear_guidelines_listing_cache should be called
        GuidelinesSectionPage.objects.create(
            path='00010002000100010002', 
            depth='5',
            landing_page_summary='Summary',
            subtitle='Overview', 
            section_colour='#28a197', 
            sub_sections_title='Topics',
            title='Test section page'
        )

        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

class GuidancePageTests(WagtailPageTests):
    fixtures = ['app.json']

    def test_guidance_page_can_only_be_created_under_section_page(self):
        # An GuidelinesSectionPage can only be created under an GuidelinesListingPage
        self.assertAllowedParentPageTypes(GuidancePage, {GuidelinesSectionPage})

    def test_guidance_page_inherits_from_translatable_page_class(self):
        assert issubclass(GuidelinesListingPage, TranslatablePage)
    
    @patch('ictcg.guidelines.models.clear_guidelines_listing_cache')
    @patch('ictcg.guidelines.models.clear_guidelines_section_cache')
    def test_clear_cache_is_called_on_save(self, mock_section, mock_listing):
        # When save is called on a GuidancePage class clear_guidelines_listing_cache and clear_guidelines_section_cache 
        # functions should be called
        GuidancePage.objects.create(
            path='000100020001000100010002', 
            depth='6',
            title='Test guidance page'
        )

        self.assertTrue(mock_section.called)
        self.assertEqual(mock_section.call_count, 1)
        self.assertTrue(mock_listing.called)
        self.assertEqual(mock_listing.call_count, 1)


class OnDeletePageSignalsTest(TestCase):
    fixtures = ['app.json']     

    @patch('ictcg.guidelines.models.clear_guidelines_listing_cache')
    @patch('ictcg.guidelines.models.clear_guidelines_section_cache')
    def test_cache_is_cleared_on_guidelines_section_page_delete(self, mock_section, mock_listing):
        # When delete is called on a GuidelinesSectionPage class clear_guidelines_section_cache should be called and 
        # clear_guidelines_listing_cache should not be called
        
        # Create a section page which has no children so we can test delete function without triggering other events based on the tree structure
        # ie, a child page also being deleted when the parent is removed
        guidelines_section_page = GuidelinesSectionPage.objects.create(
            path='00010002000100010002', 
            depth='5',
            landing_page_summary='Summary',
            subtitle='Overview', 
            section_colour='#28a197', 
            sub_sections_title='Topics',
            title='Test section page'
        )
        guidelines_section_page.delete()

        self.assertFalse(mock_section.called)
        self.assertTrue(mock_listing.called)

    @patch('ictcg.guidelines.models.clear_guidelines_listing_cache')
    @patch('ictcg.guidelines.models.clear_guidelines_section_cache')
    def test_cache_is_cleared_on_guidance_page_delete(self, mock_section, mock_listing):
        # When delete is called on a GuidancePage class clear_guidelines_section_cache and
        # clear_guidelines_listing_cache should both be called
        guidance_page = GuidancePage.objects.get(pk=8)
        guidance_page.delete()

        self.assertTrue(mock_section.called)
        self.assertTrue(mock_listing.called)
