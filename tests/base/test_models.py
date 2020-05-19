from django.test import TestCase

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from wagtailtrans.models import TranslatablePage, TranslatableSiteRootPage

from ictcg.guidelines.models import GuidelinesListingPage
from ictcg.base.models import HomePage, GenericPageWithSubNav

class HomePageTests(WagtailPageTests):

    def test_homepage_can_be_created_under_translatablesitetootpage(self):
        # You can create a HomePage under an the TranslatableSiteRootPage
        self.assertCanCreateAt(TranslatableSiteRootPage, HomePage)

    def test_listing_page_can_be_created_under_homepage(self):
        # You can create a GuidelinesSectionPage under the HomePage
        self.assertCanCreateAt(HomePage, GuidelinesListingPage)

    def test_listing_page_inherits_from_translatable_page_class(self):
        assert issubclass(HomePage, TranslatablePage)

class GenericPageWithSubNavTests(WagtailPageTests):

    def test_generic_page_can_be_created_under_homepage(self):
        # You can create a GenericPageWithSubNav under an the HomePage
        self.assertCanCreateAt(HomePage, GenericPageWithSubNav)

    def test_generic_page_can_be_nested_under_itself(self):
        # You can nested a GenericPageWithSubNav under itself
        self.assertCanCreateAt(GenericPageWithSubNav, GenericPageWithSubNav)

    def test_generic_page_inherits_from_translatable_page_class(self):
        assert issubclass(GenericPageWithSubNav, TranslatablePage)
