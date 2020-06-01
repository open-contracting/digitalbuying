from django.test import TestCase
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
    # PK 11 - case-study-number-2 - 2020-06-01
    # PK 10 - case-study-number-1 - 2020-05-31
    # PK 12 - case-study-number-3 - 2020-05-01

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

        self.assertEquals(featured_case_study.pk, 11)
        self.assertEquals(case_studies[0].pk, 10)
        self.assertEquals(case_studies[1].pk, 12)

class CaseStudyGuidelinesSectionTagTests(WagtailPageTests):

    def test_case_study_section_tags_class_inherits_from_tagged_itme_base_class(self):
        assert issubclass(CaseStudyGuidelinesSectionTag, TaggedItemBase)

# import pudb; pu.db()
class CaseStudyPageTests(WagtailPageTests):
    fixtures = ['app.json']
    # Order of case studies should as below based on publication date (newest first)
    # PK 11 - case-study-number-2 - 2020-06-01
    # PK 10 - case-study-number-1 - 2020-05-31
    # PK 12 - case-study-number-3 - 2020-05-01

    def test_case_study_page_can_be_created_under_case_study_listing_page(self):
        # You can create a GenericPageWithSubNav under an the HomePage
        self.assertCanCreateAt(CaseStudiesListingPage, CaseStudyPage)

    def test_case_study_page_can_not_be_nested_under_itself(self):
        # You can nested a GenericPageWithSubNav under itself
        self.assertCanNotCreateAt(CaseStudyPage, CaseStudyPage)

    def test_case_studies_article_pagination_links_ordered_by_publication_date_first_page(self):
        # The first article (order by publication_date) should have a next page link and not a prev link
        response = self.client.get('/en/case-studies/case-study-number-2/') #PK 11
        
        self.assertFalse('prev_sibling' in response.context)
        self.assertTrue('next_sibling' in response.context)
        self.assertEquals(response.context['next_sibling'].pk, 10)
    
    def test_case_studies_article_pagination_links_ordered_by_publication_date_middle_page(self):
        # A middle page  article (order by publication_date) should have a next page link and a prev link
        response = self.client.get('/en/case-studies/case-study-number-1/') #PK 10
        
        self.assertTrue('prev_sibling' in response.context)
        self.assertTrue('next_sibling' in response.context)
        self.assertEquals(response.context['prev_sibling'].pk, 11)
        self.assertEquals(response.context['next_sibling'].pk, 12)

    def test_case_studies_article_pagination_links_ordered_by_publication_date_lasr_page(self):
        # The last page (order by publication_date) should have a prev link but no next link
        response = self.client.get('/en/case-studies/case-study-number-3/') #PK 12
        
        self.assertTrue('prev_sibling' in response.context)
        self.assertFalse('next_sibling' in response.context)
        self.assertEquals(response.context['prev_sibling'].pk, 10)
