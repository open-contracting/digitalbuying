from django.test import TestCase
from unittest.mock import Mock, patch
from django.core.exceptions import ValidationError

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests
from wagtailtrans.models import TranslatablePage, TranslatableSiteRootPage
from wagtail.images.models import Image

from taggit.models import TaggedItemBase

from ictcg.case_studies.models import CaseStudiesListingPage, CaseStudyPage, CaseStudyGuidelinesSectionTag
from ictcg.base.models import HomePage

class CaseStudiesListingPageTests(WagtailPageTests):
    fixtures = ['app.json']
    # Order of case studies should as below based on publication date (newest first)
    # PK 13 - case-study-number-2 - 2020-06-01
    # PK 12 - case-study-number-1 - 2020-05-31
    # PK 14 - case-study-number-3 - 2020-05-01

    def test_case_studies_listing_page_can_be_created_under_homepage(self):
        # You can create a CaseStudiesListingPage under an HomePage
        self.assertCanCreateAt(HomePage, CaseStudiesListingPage)

    def test_section_page_can_be_created_under_listing_page(self):
        # You can create a CaseStudyPage under an CaseStudiesListingPage
        self.assertCanCreateAt(CaseStudiesListingPage, CaseStudyPage)

    def test_listing_page_inherits_from_translatable_page_class(self):
        assert issubclass(CaseStudiesListingPage, TranslatablePage)

    def test_case_studies_listing_context(self):
        # Test we get the correct featured article from the context based on publication_date
        # Also test the correct order of standard articles based on same publication_date
        response = self.client.get('/en/case-studies/')
        featured_case_study = response.context['featured_case_studies']
        case_studies = response.context['case_studies']

        self.assertEqual(featured_case_study.pk, 13)
        self.assertEqual(case_studies[0].pk, 12)
        self.assertEqual(case_studies[1].pk, 14)

class CaseStudyGuidelinesSectionTagTests(WagtailPageTests):

    def test_case_study_section_tags_class_inherits_from_tagged_itme_base_class(self):
        assert issubclass(CaseStudyGuidelinesSectionTag, TaggedItemBase)

class CaseStudyPageTests(WagtailPageTests):
    fixtures = ['app.json']
    # Order of case studies should as below based on publication date (newest first)
    # PK 13 - case-study-number-2 - 2020-06-01
    # PK 12 - case-study-number-1 - 2020-05-31
    # PK 14 - case-study-number-3 - 2020-05-01

    def test_case_study_page_can_be_created_under_case_study_listing_page(self):
        # You can create a GenericPageWithSubNav under an the HomePage
        self.assertCanCreateAt(CaseStudiesListingPage, CaseStudyPage)

    def test_case_study_page_can_not_be_nested_under_itself(self):
        # You can nested a GenericPageWithSubNav under itself
        self.assertCanNotCreateAt(CaseStudyPage, CaseStudyPage)

    def test_case_studies_article_pagination_links_ordered_by_publication_date_first_page(self):
        # The first article (order by publication_date) should have a next page link and not a prev link
        response = self.client.get('/en/case-studies/case-study-number-2/') #PK 13
        
        self.assertFalse('prev_page' in response.context)
        self.assertTrue('next_page' in response.context)
        self.assertEqual(response.context['next_page'].pk, 12)
    
    def test_case_studies_article_pagination_links_ordered_by_publication_date_middle_page(self):
        # A middle page  article (order by publication_date) should have a next page link and a prev link
        response = self.client.get('/en/case-studies/case-study-number-1/') #PK 12
        
        self.assertTrue('prev_page' in response.context)
        self.assertTrue('next_page' in response.context)
        self.assertEqual(response.context['prev_page'].pk, 13)
        self.assertEqual(response.context['next_page'].pk, 14)

    def test_case_studies_article_pagination_links_ordered_by_publication_date_lasr_page(self):
        # The last page (order by publication_date) should have a prev link but no next link
        response = self.client.get('/en/case-studies/case-study-number-3/') #PK 14
        
        self.assertTrue('prev_page' in response.context)
        self.assertFalse('next_page' in response.context)
        self.assertEqual(response.context['prev_page'].pk, 12)
    
    @patch('ictcg.case_studies.models.clear_case_study_cache')
    def test_clear_cache_is_called_on_save(self, mock):
        # When save is called on a CaseStudyPage class clear_case_study_cache should be called
        case_study = CaseStudyPage.objects.get(id='13')
        case_study.save()

        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)
        