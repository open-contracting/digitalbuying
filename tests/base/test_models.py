from django.test import TestCase
from django.core.exceptions import ValidationError

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests
from wagtailtrans.models import TranslatablePage, TranslatableSiteRootPage
from wagtail.images.models import Image

from ictcg.guidelines.models import GuidelinesListingPage
from ictcg.base.models import CookiePage, GenericPage, GenericPageWithSubNav, HomePage
from ictcg.case_studies.models import CaseStudiesListingPage
from ictcg.sponsors.models import SponsorsPage

class HomePageTests(WagtailPageTests):
    fixtures = ['app.json']

    def test_homepage_can_be_created_under_translatablesitetootpage(self):
        # You can create a HomePage under an the TranslatableSiteRootPage
        self.assertCanCreateAt(TranslatableSiteRootPage, HomePage)

    def test_listing_page_can_be_created_under_homepage(self):
        # You can create a GuidelinesSectionPage under the HomePage
        self.assertCanCreateAt(HomePage, GuidelinesListingPage)
    
    def test_generic_page_with_sub_nav_can_be_created_under_homepage(self):
        # You can create a CaseStudiesListingPage under the HomePage
        self.assertCanCreateAt(HomePage, GenericPageWithSubNav)
    
    def test_generic_page_can_be_created_under_homepage(self):
        # You can create a GenericPage under the HomePage
        self.assertCanCreateAt(HomePage, GenericPage)

    def test_case_studies_listing_page_can_be_created_under_homepage(self):
        # You can create a CaseStudiesListingPage under the HomePage
        self.assertCanCreateAt(HomePage, CaseStudiesListingPage)
    
    def test_cookie_page_can_be_created_under_homepage(self):
        # You can create a CaseStudiesListingPage under the HomePage
        self.assertCanCreateAt(HomePage, CookiePage)
    
    def test_sponsors_page_can_be_created_under_homepage(self):
        # You can create a SponsorsPage under the HomePage
        self.assertCanCreateAt(HomePage, SponsorsPage)

    def test_listing_page_inherits_from_translatable_page_class(self):
        assert issubclass(HomePage, TranslatablePage)

    def test_validation_error_when_masthead_image_set_but_masthead_image_description_is_missing(self):
        image = Image.objects.get(id=1)
        with self.assertRaises(ValidationError):
            HomePage.objects.create(
                title='Home', 
                masthead_title='test title', 
                masthead_description='desc', 
                masthead_image=image, 
                path='0002', 
                depth=1
            )

class GenericPageTests(WagtailPageTests):

    def test_generic_page_can_be_created_under_homepage(self):
        # You can create GenericPage under the HomePage
        self.assertCanCreateAt(HomePage, GenericPage)

    def test_generic_page_can_be_nested_under_itself(self):
        # You can nested GenericPage under itself
        self.assertCanCreateAt(GenericPage, GenericPage)

    def test_generic_page_can_be_nested_under_generic_page_with_sub_nav(self):
        # You can nested GenericPage under a GenericPageWithSubNav page
        self.assertCanCreateAt(GenericPageWithSubNav, GenericPage)
    
    def test_sponsors_page_can_be_created_under_generic_page(self):
        # You can create a SponsorsPage under a GenericPage
        self.assertCanCreateAt(GenericPage, SponsorsPage)

    def test_generic_page_inherits_from_translatable_page_class(self):
        assert issubclass(GenericPageWithSubNav, TranslatablePage)

class GenericPageWithSubNavTests(WagtailPageTests):

    def test_generic_page_with_sub_nav_can_be_created_under_homepage(self):
        # You can create a GenericPageWithSubNav under the HomePage
        self.assertCanCreateAt(HomePage, GenericPageWithSubNav)

    def test_generic_page_with_sub_nav_can_be_nested_under_itself(self):
        # You can nested GenericPageWithSubNav under itself
        self.assertCanCreateAt(GenericPageWithSubNav, GenericPageWithSubNav)

    def test_generic_page_with_sub_nav_can_be_created_under_generic_page(self):
        # You can nested GenericPageWithSubNav under GenericPage
        self.assertCanCreateAt(GenericPage, GenericPageWithSubNav)
    
    def test_sponsors_page_can_be_created_under_generic_page_with_sub_nav(self):
        # You can create a SponsorsPage under a GenericPageWithSubNav
        self.assertCanCreateAt(GenericPageWithSubNav, SponsorsPage)

    def test_generic_page_inherits_from_translatable_page_class(self):
        assert issubclass(GenericPageWithSubNav, TranslatablePage)

class CookiePageTests(WagtailPageTests):

    def test_cookie_page_can_be_created_under_homepage(self):
        # You can create a CookiePage under an the HomePage
        self.assertCanCreateAt(HomePage, CookiePage)

    def test_cookie_page_cannot_have_any_nested_pages(self):
        # You shouldn't be able to nested pages under CookiePage
        self.assertCanNotCreateAt(CookiePage, GenericPageWithSubNav)

    def test_generic_page_inherits_from_translatable_page_class(self):
        assert issubclass(GenericPageWithSubNav, TranslatablePage)