from unittest.mock import patch

from django.test import TestCase
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from wagtail.tests.utils import WagtailPageTests
from wagtailtrans.models import TranslatablePage

from base.models import GenericPage, GenericPageWithSubNav, HomePage
from sponsors.models import Sponsor, SponsorItem, SponsorsPage, clear_sponsors_footer_cache


class SponsorTests(TestCase):
    fixtures = ["sponsors.json"]

    def test_sponsor_inherits_from_clusterable_model_class(self):
        assert issubclass(Sponsor, ClusterableModel)

    def test_sponsor_object_name(self):
        sponsor = Sponsor.objects.get(language="en")
        object_string = f"Sponsors - {sponsor.language}"
        self.assertEqual(object_string, str(sponsor))

    @patch("sponsors.models.clear_sponsors_footer_cache")
    def test_clear_sponsors_footer_cache_is_called_on_save(self, mock):
        sponsor = Sponsor.objects.get(language="en")
        sponsor.save()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch("sponsors.models.clear_sponsors_footer_cache")
    def test_clear_sponsors_footer_cache_is_triggered_by_signal_on_model_delete(self, mock):
        sponsor = Sponsor.objects.get(language="en")
        sponsor.delete()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)


class SponsorItemTests(TestCase):
    fixtures = ["sponsors.json"]

    def test_sponsor_item_inherits_from_orderable_class(self):
        assert issubclass(SponsorItem, Orderable)


class ClearSponsorFooterCacheTest(TestCase):
    @patch("django.core.cache.cache.delete_many")
    def test_delete_many_is_called_when_clear_sponsors_footer_cache_is_called(self, mock):
        clear_sponsors_footer_cache("en")
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)


class SponsorsPageTests(WagtailPageTests):
    def test_sponsors_page_can_be_created_under_homepage(self):
        # You can create a SponsorsPage under the HomePage
        self.assertCanCreateAt(HomePage, SponsorsPage)

    def test_sponsors_page_cannot_be_nested_under_itself(self):
        # You cannot nested SponsorsPage under itself
        self.assertCanNotCreateAt(SponsorsPage, SponsorsPage)

    def test_sponsors_page_can_be_created_under_generic_page(self):
        # You can nested SponsorsPage under GenericPage
        self.assertCanCreateAt(GenericPage, SponsorsPage)

    def test_sponsors_page_can_be_created_under_generic_page_with_sub_nav(self):
        # You can nested SponsorsPage under GenericPageWithSubNav
        self.assertCanCreateAt(GenericPageWithSubNav, SponsorsPage)

    def test_generic_page_inherits_from_translatable_page_class(self):
        assert issubclass(SponsorsPage, TranslatablePage)
