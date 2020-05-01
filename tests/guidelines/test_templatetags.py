
from wagtail.tests.utils import WagtailPageTests
from ictcg.guidelines.templatetags.guidelines_tags import hex_to_rgb

class TemplateTagsTests(WagtailPageTests):

  def test_hex_to_rgb_tag(self):
    #check the returned value is as expected
    reg_value = hex_to_rgb('#28a197')
    self.assertEquals(reg_value, '40,161,151')
