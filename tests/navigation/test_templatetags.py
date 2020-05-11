from django.test import TestCase
from django.test.client import Client
from django.template import Context, Template
from unittest.mock import Mock, patch

from wagtail.tests.utils import WagtailPageTests

from django.db.models import Model

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

class TemplateTagsBreadcrumbTests(WagtailPageTests):
    fixtures = ['app.json']

    def test_breadcrumbs_template_returns_correct_html(self):
        TEMPLATE = Template("{% load navigation_tags %} {% breadcrumbs %}")

        guidelines_page = Page.objects.get(id=6)
        context = Context({'self': guidelines_page, 'request': []})
        template_to_render = Template(
            '{% load navigation_tags %}'
            '{% breadcrumbs %}'
        )
    
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<a class="ictcg-breadcrumbs__link" href="/en/">Home</a>', rendered_template)

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
        # Get guidance page, depth of the page should be 6
        # Parent depth should be 1 less (5)
        guidance_page = Page.objects.get(id=8)
        ancestors = Page.objects.ancestor_of(guidance_page, inclusive=True).filter(depth__gt=2)
        parent = get_parent(ancestors, guidance_page.depth)
        self.assertEqual(parent.depth, guidance_page.depth - 1)
        self.assertEqual(parent.depth, 5)

class TemplateTagsMainMenuTests(WagtailPageTests):
    fixtures = ['navigation.json', 'app.json']

    def setUp(self):
        self.client = Client()

    def test_get_main_menu_from_selected_language(self):
        # Get main menu based on the selected languauge
        menu = main_menu('en')
        object_string = f'{menu.title} - {menu.language}'
        self.assertEquals(object_string, str(menu))

    def test_get_main_menu_when_no_language_passed(self):
        # When a menu is not found, should return english by default
        menu = main_menu('it')
        self.assertEquals('main menu - en', str(menu))

    def test_is_main_menu_link_active(self):
        # Should return true when the menu item link property is also in the requested url
        response = self.client.get('/en/guidelines')
        context = {'request': response.wsgi_request}
        self.assertTrue(is_main_menu_link_active(context, 'guidelines'))
        

class TemplateTagsFooterTests(WagtailPageTests):
    fixtures = ['navigation.json', 'app.json']

    def test_get_footer_content(self):
        # Get Footer based on the selected language
        footer = get_footer_content('en')

        self.assertTrue('guildelines_sections' in footer)
        self.assertTrue('guildelines_title' in footer)
        self.assertTrue('footer_content' in footer)
        self.assertEqual(len(footer), 3)
      