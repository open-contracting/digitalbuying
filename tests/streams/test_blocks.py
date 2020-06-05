from wagtail.tests.utils import WagtailPageTests
from wagtail.core import blocks
from ictcg.streams import blocks as ictgs_blocks


class RichTextBlockTests(WagtailPageTests):
    def test_rich_text_block_subclass(self):
        assert issubclass(ictgs_blocks.RichTextWithTitleBlock, blocks.StructBlock)

    def test_rich_text_block(self):
        child_blocks = ictgs_blocks.RichTextWithTitleBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['hide_horizontal_rule']) is blocks.BooleanBlock
        assert type(child_blocks['content']) is blocks.RichTextBlock

    def test_rich_text_block_count(self):
        child_blocks = ictgs_blocks.RichTextWithTitleBlock().child_blocks
        self.assertEquals(len(child_blocks), 3)

    def test_rich_text_block_template(self):
        self.assertEquals(ictgs_blocks.RichTextWithTitleBlock().get_template(), 'streams/richtext_block.html')

class TextAlignmentBlockTests(WagtailPageTests):
    def test_text_alignment_block_subclass(self):
        assert issubclass(ictgs_blocks.TextAlignmentBlock, blocks.ChoiceBlock)


class HomePageRichTextBlockTests(WagtailPageTests):
    def test_home_page_rich_text_block_subclass(self):
        assert issubclass(ictgs_blocks.HomePageRichTextBlock, blocks.StructBlock)

    def test_home_page_rich_text_block(self):
        child_blocks = ictgs_blocks.HomePageRichTextBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['width']) is blocks.ChoiceBlock
        assert type(child_blocks['text_alignment']) is ictgs_blocks.TextAlignmentBlock
        assert type(child_blocks['content']) is blocks.RichTextBlock

    def test_home_page_rich_text_block_count(self):
        child_blocks = ictgs_blocks.HomePageRichTextBlock().child_blocks
        self.assertEquals(len(child_blocks), 4)

    def test_home_page_rich_text_block_template(self):
        self.assertEquals(ictgs_blocks.HomePageRichTextBlock().get_template(), 'streams/homepage_richtext_block.html')


class HighlightListBlockTests(WagtailPageTests):
    def test_highlight_list_block_subclass(self):
        assert issubclass(ictgs_blocks.HighlightListBlock, blocks.StructBlock)

    def  test_highlight_list_block(self):
        child_blocks = ictgs_blocks.HighlightListBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['items_list']) is blocks.ListBlock

    def test_highlight_list_block_count(self):
        child_blocks = ictgs_blocks.HighlightListBlock().child_blocks
        self.assertEquals(len(child_blocks), 2)

    def test_highlight_list_block_template(self):
        self.assertEquals(ictgs_blocks.HighlightListBlock().get_template(), 'streams/highlight_list_block.html')


class CaseStudyBlockTests(WagtailPageTests):
    def test_case_study_block_subclass(self):
        assert issubclass(ictgs_blocks.CaseStudyBlock, blocks.StructBlock)

    def test_case_study_block(self):
        child_blocks = ictgs_blocks.CaseStudyBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['text_alignment']) is ictgs_blocks.TextAlignmentBlock
        assert type(child_blocks['content']) is blocks.RichTextBlock
        assert type(child_blocks['button_text']) is blocks.CharBlock
        assert type(child_blocks['button_link']) is blocks.PageChooserBlock

    def test_case_study_block_count(self):
        child_blocks = ictgs_blocks.CaseStudyBlock().child_blocks
        self.assertEquals(len(child_blocks), 5)

    def test_case_study_block_template(self):
        self.assertEquals(ictgs_blocks.CaseStudyBlock().get_template(), 'streams/case_study_block.html')

class DoDontCardTests(WagtailPageTests):
    def test_do_dont_card_subclass(self):
        assert issubclass(ictgs_blocks.DoOrDontCard, blocks.StructBlock)
    
    def test_do_dont_card_input_types(self):
        child_blocks = ictgs_blocks.DoOrDontCard().child_blocks
        assert type(child_blocks['item']) is blocks.CharBlock
    
    def test_do_dont_card_input_types_count(self):
        child_blocks = ictgs_blocks.DoOrDontCard().child_blocks
        self.assertEquals(len(child_blocks), 1)

class DoDontBlockTests(WagtailPageTests):
    def test_do_dont_block_subclass(self):
        assert issubclass(ictgs_blocks.DosAndDontsBlock, blocks.StructBlock)

    def test_do_dont_block_input_types(self):
        child_blocks = ictgs_blocks.DosAndDontsBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['dos']) is blocks.ListBlock
        assert type(child_blocks['donts']) is blocks.ListBlock
    
    def test_do_dont_block_input_types_count(self):
        child_blocks = ictgs_blocks.DosAndDontsBlock().child_blocks
        self.assertEquals(len(child_blocks), 3)

    def test_do_dont_block_template(self):
        self.assertEquals(ictgs_blocks.DosAndDontsBlock().get_template(), 'streams/do_dont_list.html')

class QuoteBlockTests(WagtailPageTests):
    def test_quote_block_subclass(self):
        assert issubclass(ictgs_blocks.QuoteBlock, blocks.StructBlock)

    def test_quote_block_input_types(self):
        child_blocks = ictgs_blocks.QuoteBlock().child_blocks
        assert type(child_blocks['title']) is blocks.CharBlock
        assert type(child_blocks['hide_horizontal_rule']) is blocks.BooleanBlock
        assert type(child_blocks['content_top']) is blocks.RichTextBlock
        assert type(child_blocks['quote']) is blocks.CharBlock
        assert type(child_blocks['attribution']) is blocks.CharBlock
        assert type(child_blocks['content_bottom']) is blocks.RichTextBlock
    
    def test_do_dont_block_input_types_count(self):
        child_blocks = ictgs_blocks.QuoteBlock().child_blocks
        self.assertEquals(len(child_blocks), 6)

    def test_quote_block_template(self):
        self.assertEquals(ictgs_blocks.QuoteBlock().get_template(), 'streams/quote_block.html')
