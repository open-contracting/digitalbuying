from django.test import TestCase

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

  def test_section_page_can_only_be_created_under_list_page(self):
    # An GuidelinesSectionPage can only be created under an GuidelinesListingPage
    self.assertAllowedParentPageTypes(GuidelinesSectionPage, {GuidelinesListingPage})
  
  def test_guidance_page_can_be_created_under_sectiong_page(self):
    # An GuidancePage can be created inder an GuidelinesListingPage
    self.assertCanCreateAt(GuidelinesSectionPage, GuidancePage)

  def test_section_page_inherits_from_translatable_page_class(self):
      assert issubclass(GuidelinesListingPage, TranslatablePage)

class GuidancePageTests(WagtailPageTests):

  def test_guidance_page_can_only_be_created_under_section_page(self):
    # An GuidelinesSectionPage can only be created under an GuidelinesListingPage
    self.assertAllowedParentPageTypes(GuidancePage, {GuidelinesSectionPage})

  def test_guidance_page_inherits_from_translatable_page_class(self):
    assert issubclass(GuidelinesListingPage, TranslatablePage)
