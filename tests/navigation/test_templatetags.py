from django.test import TestCase
from django.template import Context, Template
from django.db.models import Model
from unittest.mock import Mock, patch
from django.conf import settings

from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable

from ictcg.navigation.models import MainMenu
from ictcg.navigation.templatetags.navigation_tags import (
    breadcrumbs, 
    get_parent, 
    main_menu, 
    is_main_menu_link_active, 
    get_footer_content
)

class TemplateTagsBreadcrumbTests(TestCase):
    fixtures = ['app.json']

    def test_breadcrumbs_template_returns_correct_html(self):
        response = self.client.get('/en/guidelines/') #PK 6
        self.assertInHTML('<a class="ictcg-breadcrumbs__link" href="/en/">Home</a>', response.rendered_content.strip())
        self.assertInHTML('<li class="ictcg-breadcrumbs__list-item" aria-current="page">Guidelines</li>', response.rendered_content.strip())


    def test_breadcrumbs_return_correct_ancestor_data(self):
        # Get guidelines section page
        # This is a level 3 page in the UI (Level 5 in database due to the parent root pages).  Home > Guidelines > Guidelines section
        guidelines_page = Page.objects.get(id=7) 
        data = breadcrumbs({'self': guidelines_page, 'request': []})
        ancestors = data['ancestors']
        parent = data['parent']

        self.assertEqual(len(ancestors), 3)
        self.assertEqual(parent.title, 'Guidelines')
    
    def test_get_parent(self):
        # Get guidance page (ID 9), depth of the page should be 6
        # Parent depth should be 1 less (5)
        guidance_page = Page.objects.get(id=9)
        ancestors = Page.objects.ancestor_of(guidance_page, inclusive=True).filter(depth__gt=2)
        parent = get_parent(ancestors, guidance_page.depth)
        self.assertEqual(parent.depth, guidance_page.depth - 1)
        self.assertEqual(parent.depth, 5)

class TemplateTagsMainMenuTests(TestCase):
    fixtures = ['navigation.json', 'app.json']

    def test_get_main_menu_from_selected_language(self):
        # Get main menu based on the selected languauge
        menu = main_menu('en')
        language = dict(settings.LANGUAGES)
        object_string = f'{menu.title} - {language[menu.language]}'
        self.assertEquals(object_string, str(menu))

    def test_get_main_menu_when_no_language_passed(self):
        # When a menu is not found, should return english by default
        menu = main_menu('it')
        self.assertEquals('main menu - English', str(menu))

    def test_is_main_menu_link_active(self):
        # Should return true when the menu item link property is also in the requested url
        response = self.client.get('/en/guidelines')
        context = {'request': response.wsgi_request}
        self.assertTrue(is_main_menu_link_active(context, 'guidelines'))
        

class TemplateTagsFooterTests(TestCase):
    fixtures = ['navigation.json', 'app.json']

    def test_get_footer_content(self):
        # Get Footer based on the selected language
        footer = get_footer_content()

        self.assertTrue('guildelines_sections' in footer)
        self.assertTrue('guildelines_title' in footer)
        self.assertTrue('footer_content' in footer)
        self.assertEqual(len(footer), 3)
      