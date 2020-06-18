from django.test import TestCase
from unittest.mock import Mock, patch
from django.conf import settings
from django.db.models import Model

from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable
from ictcg.sponsors.models import Sponsor, SponsorItem, clear_sponsors_footer_cache

class SponsorTests(TestCase):
	fixtures = ['sponsors.json']

	def test_sponsor_inherits_from_clusterable_model_class(self):
		assert issubclass(Sponsor, ClusterableModel)

	def test_sponsor_object_name(self):
		sponsor = Sponsor.objects.get(language="en")
		object_string = f'Sponsors - {sponsor.language}'
		self.assertEquals(object_string, str(sponsor))
	
	@patch('ictcg.sponsors.models.clear_sponsors_footer_cache')
	def test_clear_sponsors_footer_cache_is_called_on_save(self, mock):
		sponsor = Sponsor.objects.get(language="en")
		sponsor.save()
		self.assertTrue(mock.called)
		self.assertEqual(mock.call_count, 1)

	@patch('ictcg.sponsors.models.clear_sponsors_footer_cache')
	def test_clear_sponsors_footer_cache_is_triggered_by_signal_on_model_delete(self, mock):
		sponsor = Sponsor.objects.get(language="en")
		sponsor.delete()
		self.assertTrue(mock.called)
		self.assertEqual(mock.call_count, 1)

class SponsorItemTests(TestCase):
	fixtures = ['sponsors.json']

	def test_sponsor_item_inherits_from_orderable_class(self):
		assert issubclass(SponsorItem, Orderable)

class ClearSponsorFooterCacheTest(TestCase):
	@patch('django.core.cache.cache.delete_many')
	def test_delete_many_is_called_when_clear_sponsors_footer_cache_is_called(self, mock):
		clear_sponsors_footer_cache('en')
		self.assertTrue(mock.called)
		self.assertEqual(mock.call_count, 1)

	