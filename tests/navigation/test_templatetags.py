from django.test import TestCase
from django.template import Context, Template
from unittest.mock import Mock, patch

from wagtail.tests.utils import WagtailPageTests

from django.db.models import Model

from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable

from ictcg.navigation.templatetags.navigation_tags import breadcrumbs

# import pudb; pu.db()

class TemplateTagsTests(WagtailPageTests):
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
        # This is a level 3 page.  Home > Guidelines > Guidelines section
        guidelines_page = Page.objects.get(id=7) 
        data = breadcrumbs({'self': guidelines_page, 'request': []})
        ancestors = data['ancestors']
        parent = data['parent']

        self.assertEqual(len(ancestors), 3)
        self.assertEqual(parent.title, 'Guidelines')