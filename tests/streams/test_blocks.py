from wagtail.tests.utils import WagtailPageTests
from wagtail.core import blocks
from ictcg.streams import blocks as ictgs_blocks

class StreamBlockTests(WagtailPageTests):
  def test_rich_text_block(self):
    assert issubclass(ictgs_blocks.RichTextWithTitleBlock, blocks.StructBlock)
    child_blocks = ictgs_blocks.RichTextWithTitleBlock().child_blocks
    assert type(child_blocks['title']) is blocks.CharBlock
    assert type(child_blocks['content']) is blocks.RichTextBlock
  
  def test_rich_text_block_template(self):
    self.assertEquals(ictgs_blocks.RichTextWithTitleBlock().get_template(), 'streams/richtext_block.html')
  
  def test_do_dont_card_block(self):
    assert issubclass(ictgs_blocks.DoOrDontCard, blocks.StructBlock)
    child_blocks = ictgs_blocks.DoOrDontCard().child_blocks
    assert type(child_blocks['item']) is blocks.CharBlock

  def test_do_dont_block(self):
    assert issubclass(ictgs_blocks.DosAndDontsBlock, blocks.StructBlock)
    child_blocks = ictgs_blocks.DosAndDontsBlock().child_blocks
    assert type(child_blocks['title']) is blocks.CharBlock
    assert type(child_blocks['dos']) is blocks.ListBlock
    assert type(child_blocks['donts']) is blocks.ListBlock
  
  def test_do_dont_block_template(self):
    self.assertEquals(ictgs_blocks.DosAndDontsBlock().get_template(), 'streams/do_dont_list.html')
