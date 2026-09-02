from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from navigation import models


class MainMenuTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.MainMenu.objects.create(title="test title 1", language="en")

    def test_mainmenu_object_name(self):
        main_menu = models.MainMenu.objects.get(title__exact="test title 1")
        language = dict(settings.LANGUAGES)
        object_string = f"{main_menu.title} - {language[main_menu.language]}"
        self.assertEqual(object_string, str(main_menu))

    @patch("navigation.models.clear_mainmenu_cache")
    def test_clear_mainmenu_cache_is_called_on_save(self, mock):
        main_menu = models.MainMenu.objects.get(title__exact="test title 1")
        main_menu.save()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)


class FooterMenuTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.FooterMenu.objects.create(admin_title="Footer title 1", language="en")

    def test_footermenu_object_name(self):
        footer_menu = models.FooterMenu.objects.get(admin_title__exact="Footer title 1")
        language = dict(settings.LANGUAGES)
        object_string = f"{footer_menu.admin_title} - {language[footer_menu.language]}"
        self.assertEqual(object_string, str(footer_menu))

    @patch("navigation.models.clear_footer_cache")
    def test_clear_footer_cache_is_called_on_save(self, mock):
        footer_menu = models.FooterMenu.objects.get(admin_title__exact="Footer title 1")
        footer_menu.save()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)


class ClearMainMenuCacheTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.MainMenu.objects.create(title="test title 1", language="en")

    @patch("django.core.cache.cache.delete")
    def test_delete_is_called_when_clear_mainmenu_cache_is_called(self, mock):
        models.clear_mainmenu_cache("en")
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch("navigation.models.clear_mainmenu_cache")
    def test_clear_mainmenu_cache_is_triggered_by_signal_on_model_delete(self, mock):
        main_menu = models.MainMenu.objects.get(title__exact="test title 1")
        main_menu.delete()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)


class ClearFooterCacheTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.FooterMenu.objects.create(admin_title="Footer title 2", language="en")

    @patch("django.core.cache.cache.delete_many")
    def test_delete_is_called_when_clear_footer_cache_is_called(self, mock):
        models.clear_footer_cache("en")
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch("navigation.models.clear_footer_cache")
    def test_clear_footer_cache_is_triggered_by_signal_on_model_delete(self, mock):
        footer_menu = models.FooterMenu.objects.get(admin_title__exact="Footer title 2")
        footer_menu.delete()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)
