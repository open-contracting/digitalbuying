from django.test import TestCase

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from wagtailtrans.models import TranslatablePage, TranslatableSiteRootPage

from ictcg.guidelines.models import GuidelinesListingPage
from ictcg.base.models import HomePage

class HomePageTests(WagtailPageTests):

    def test_listing_page_can_be_created_under_homepage(self):
        # You can create a HomePage under an the TranslatableSiteRootPage
        self.assertCanCreateAt(TranslatableSiteRootPage, HomePage)

    def test_section_page_can_be_created_under_listing_page(self):
        # You can create a GuidelinesSectionPage under the HomePage
        self.assertCanCreateAt(HomePage, GuidelinesListingPage)

    def test_listing_page_inherits_from_translatable_page_class(self):
        assert issubclass(HomePage, TranslatablePage)
