from wagtail.tests.utils import WagtailPageTests
from wagtail.core import blocks
from ictcg.streams import blocks as ictgs_blocks


class RichTextBlockTests(WagtailPageTests):
    def test_rich_text_block_subclass(self):
        assert issubclass(ictgs_blocks.RichTextWithTitleBlock, blocks.StructBlock)

    def test_rich_text_block(self):
        child_blocks = ictgs_blocks.RichTextWithTitleBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['content']) is blocks.RichTextBlock

    def test_rich_text_block_template(self):
        self.assertEquals(ictgs_blocks.RichTextWithTitleBlock().get_template(), 'streams/richtext_block.html')

class DoDontCardTests(WagtailPageTests):
    def test_do_dont_card_subclass(self):
        assert issubclass(ictgs_blocks.DoOrDontCard, blocks.StructBlock)
    
    def test_do_dont_card_input_types(self):
        child_blocks = ictgs_blocks.DoOrDontCard().child_blocks
        assert type(child_blocks['item']) is blocks.CharBlock

class DoDontBlockTests(WagtailPageTests):
    def test_do_dont_block_subclass(self):
        assert issubclass(ictgs_blocks.DosAndDontsBlock, blocks.StructBlock)

    def test_do_dont_block_input_types(self):
        child_blocks = ictgs_blocks.DosAndDontsBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['dos']) is blocks.ListBlock
        assert type(child_blocks['donts']) is blocks.ListBlock

    def test_do_dont_block_template(self):
        self.assertEquals(ictgs_blocks.DosAndDontsBlock().get_template(), 'streams/do_dont_list.html')

class QuoteBlockTests(WagtailPageTests):
    def test_quote_block_subclass(self):
        assert issubclass(ictgs_blocks.QuoteBlock, blocks.StructBlock)

    def test_quote_block_input_types(self):
        child_blocks = ictgs_blocks.QuoteBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['content_top']) is blocks.RichTextBlock
        assert type(child_blocks['quote']) is blocks.CharBlock
        assert type(child_blocks['attribution']) is blocks.CharBlock
        assert type(child_blocks['content_bottom']) is blocks.RichTextBlock

    def test_quote_block_template(self):
        self.assertEquals(ictgs_blocks.QuoteBlock().get_template(), 'streams/quote_block.html')
