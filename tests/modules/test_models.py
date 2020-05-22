from django.test import TestCase
from unittest.mock import Mock, patch

from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from wagtail.tests.utils import WagtailPageTests

from ictcg.modules.models import KeyModuleFields, Links, MoreInformationModule, OrderableLinks, LinksModule

class KeyModuleFieldsTests(WagtailPageTests):
    def test_meta_abstract_is_true(self):
        Keyfields = KeyModuleFields()
        self.assertTrue(Keyfields._meta.abstract)

    def test_key_module_fields_class_inherits_from_models_class(self):
        self.assertTrue(issubclass(KeyModuleFields, models.Model))

class LinksTests(WagtailPageTests):
    def test_links_class_inherits_from_models_class(self):
        self.assertTrue(issubclass(KeyModuleFields, models.Model))
    
    def test_meta_abstract_is_true(self):
        links = Links()
        self.assertTrue(links._meta.abstract)

class MoreInformationModuleTests(WagtailPageTests):
    def test_more_info_module_class_inherits_from_Key_module_fields(self):
        self.assertTrue(issubclass(MoreInformationModule, KeyModuleFields))

    def test_more_info_object_name(self):
        admin_title = 'hello world'
        lang = 'en'
        more_info = MoreInformationModule.objects.create(language=lang, admin_title=admin_title, title='display title')
        object_string = f'{admin_title} - {lang}'
        self.assertEquals(object_string, str(more_info))

class OrderableLinksTests(WagtailPageTests):
    def test_orderable_links_class_inherits_from_orderable_and_links_classes(self):
        self.assertTrue(issubclass(OrderableLinks, Orderable))
        self.assertTrue(issubclass(OrderableLinks, Links))

class LinksModuleTests(WagtailPageTests):
    def test_links_modules_class_inherits_from_clusterablemodel_and_key_link_fields_classes(self):
        self.assertTrue(issubclass(LinksModule, ClusterableModel))
        self.assertTrue(issubclass(LinksModule, KeyModuleFields))
    
    def test_links_modile_object_name(self):
        admin_title = 'hello again'
        lang = 'es'
        more_info = LinksModule.objects.create(language=lang, admin_title=admin_title, title='display title')
        object_string = f'{admin_title} - {lang}'
        self.assertEquals(object_string, str(more_info))
