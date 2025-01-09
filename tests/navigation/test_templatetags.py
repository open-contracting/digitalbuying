from django.conf import settings
from django.test import TestCase
from wagtail.core.models import Page

from ictcg.navigation.templatetags.navigation_tags import (
    breadcrumbs,
    get_footer_content,
    get_parent,
    is_main_menu_link_active,
    main_menu,
)


class TemplateTagsBreadcrumbTests(TestCase):
    fixtures = ["app.json"]

    def test_breadcrumbs_template_returns_correct_html(self):
        response = self.client.get("/en/guidelines/")  # PK 6
        self.assertInHTML('<a class="ictcg-breadcrumbs__link" href="/en/">Home</a>', response.rendered_content.strip())
        self.assertInHTML(
            '<li class="ictcg-breadcrumbs__list-item" aria-current="page">Guidelines</li>',
            response.rendered_content.strip(),
        )

    def test_breadcrumbs_return_correct_ancestor_data(self):
        # Get guidelines section page
        # This is a level 3 page in the UI (Level 5 in database due to the parent root pages).  Home > Guidelines > Guidelines section
        guidelines_page = Page.objects.get(id=7)
        data = breadcrumbs({"self": guidelines_page, "request": []})
        ancestors = data["ancestors"]
        parent = data["parent"]

        self.assertEqual(len(ancestors), 3)
        self.assertEqual(parent.title, "Guidelines")

    def test_get_parent(self):
        # Get guidance page (ID 9), depth of the page should be 6
        # Parent depth should be 1 less (5)
        guidance_page = Page.objects.get(id=9)
        ancestors = Page.objects.ancestor_of(guidance_page, inclusive=True).filter(depth__gt=2)
        parent = get_parent(ancestors, guidance_page.depth)
        self.assertEqual(parent.depth, guidance_page.depth - 1)
        self.assertEqual(parent.depth, 5)


class TemplateTagsMainMenuTests(TestCase):
    fixtures = ["navigation.json", "app.json"]

    def test_get_main_menu_from_selected_language(self):
        # Get main menu based on the selected languauge
        menu = main_menu("en")
        language = dict(settings.LANGUAGES)
        object_string = f"{menu.title} - {language[menu.language]}"
        self.assertEqual(object_string, str(menu))

    def test_get_main_menu_when_no_language_passed(self):
        # When a menu is not found, should return english by default
        menu = main_menu("it")
        self.assertEqual("main menu - English", str(menu))

    def test_is_main_menu_link_active(self):
        # Should return true when the menu item link property is also in the requested url
        response = self.client.get("/en/guidelines")
        context = {"request": response.wsgi_request}
        self.assertTrue(is_main_menu_link_active(context, "guidelines"))


class TemplateTagsFooterTests(TestCase):
    fixtures = ["navigation.json", "app.json"]

    def test_get_footer_content(self):
        # Get Footer based on the selected language
        footer = get_footer_content()

        self.assertTrue("guildelines" in footer)
        self.assertTrue("footer_content" in footer)
        self.assertEqual(len(footer), 2)
