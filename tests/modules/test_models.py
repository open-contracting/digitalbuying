from wagtail.test.utils import WagtailPageTestCase

from modules.models import LinksModule, MoreInformationModule


class MoreInformationModuleTests(WagtailPageTestCase):
    def test_more_info_object_name(self):
        admin_title = "hello world"
        lang = "en"
        more_info = MoreInformationModule.objects.create(language=lang, admin_title=admin_title, title="display title")
        object_string = f"{admin_title} - {lang}"
        self.assertEqual(object_string, str(more_info))


class LinksModuleTests(WagtailPageTestCase):
    def test_links_modile_object_name(self):
        admin_title = "hello again"
        lang = "es"
        more_info = LinksModule.objects.create(language=lang, admin_title=admin_title, title="display title")
        object_string = f"{admin_title} - {lang}"
        self.assertEqual(object_string, str(more_info))
