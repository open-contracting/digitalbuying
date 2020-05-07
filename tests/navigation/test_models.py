from django.test import TestCase
from unittest.mock import Mock, patch

from django.db.models import Model

from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable
from ictcg.navigation.models import *

class MainMenuTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		MainMenu.objects.create(title='test title 1', language='en')

	def test_mainmenu_inherits_from_translatable_page_class(self):
		assert issubclass(MainMenu, ClusterableModel)

	def test_mainmenu_object_name(self):
		main_menu = MainMenu.objects.get(title__exact="test title 1")
		object_string = f'{main_menu.title} - {main_menu.language}'
		self.assertEquals(object_string, str(main_menu))

class MenuItemTests(TestCase):
	fixtures = ['app.json']

	def test_mainmenu_inherits_from_translatable_page_class(self):
		assert issubclass(MenuItem, Model)

	def test_link_property_should_return_page_url_when_page_object_is_set(self):
		# Page ID 6 from fixtures - guidelines page
		guidelines_page = Page.objects.get(id=6)
		menu_item = MenuItem.objects.create(title="Menu item 1", page=guidelines_page)
		self.assertEqual(menu_item.link, guidelines_page.url)

	def test_link_property_should_return_local_url_when_page_object_is_not_set(self):
		test_url = 'http://www.test.com'
		menu_item = MenuItem.objects.create(title="Menu item 2", url=test_url)
		self.assertEqual(menu_item.link, test_url)

class MainMenuItemTests(TestCase):
	def test_mainmenuitem_inherits_from_orderable_and_menuitem_classes(self):
		assert issubclass(MainMenuItem, (Orderable, MenuItem))

class FooterMenuTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		FooterMenu.objects.create(admin_title='Footer title 1', language='en')

	def test_footermenu_inherits_from_translatable_page_class(self):
		assert issubclass(FooterMenu, ClusterableModel)

	def test_footermenu_object_name(self):
		footer_menu = FooterMenu.objects.get(admin_title__exact="Footer title 1")
		object_string = f'{footer_menu.admin_title} - {footer_menu.language}'
		self.assertEquals(object_string, str(footer_menu))
	
	@patch('ictcg.navigation.models.clear_footer_cache')
	def test_clear_footer_cache_is_called_on_save(self, mock):
		footer_menu = FooterMenu.objects.get(admin_title__exact="Footer title 1")
		footer_menu.save()
		self.assertTrue(mock.called)
		self.assertEqual(mock.call_count, 1)

class FooterMenuItemTests(TestCase):
	def test_footermenuitem_inherits_from_orderable_and_menuitem_classes(self):
		assert issubclass(FooterMenuItem, (Orderable, MenuItem))

class ClearFooterCacheTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		FooterMenu.objects.create(admin_title='Footer title 2', language='en')

	@patch('django.core.cache.cache.delete_many')
	def test_cache_delete_when_clear_footer_cache_is_called(self, mock):
		clear_footer_cache('en')
		self.assertTrue(mock.called)
		self.assertEqual(mock.call_count, 1)

	@patch('ictcg.navigation.models.clear_footer_cache')
	def test_clear_footer_cache_triggered_by_signal_on_model_delete(self, mock):
		footer_menu = FooterMenu.objects.get(admin_title__exact="Footer title 2")
		footer_menu.delete()
		self.assertTrue(mock.called)
		self.assertEqual(mock.call_count, 1)