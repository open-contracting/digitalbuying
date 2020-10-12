from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import ugettext_lazy as _


class SimpleRichTextBlock(blocks.StructBlock):
    description = blocks.CharBlock(
        max_length=120,
        help_text=_("Non visible description, max length 120 characters, used for html id.")
    )
    content = blocks.RichTextBlock()

    class Meta:
        template = "streams/simple_richtext_block.html"


class RichTextWithTitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120, help_text=_("Section title, max length 120 characters"))
    content = blocks.RichTextBlock()

    class Meta:
        template = "streams/richtext_with_title_block.html"


class TextAlignmentBlock(blocks.ChoiceBlock):
    choices = [
        ('left', 'Left'),
        ('centre', 'Centred'),
        ('right', 'Right'),
    ]


class HomePageRichTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120, required=False, help_text=_("Section title, max length 120 characters"))

    width = blocks.ChoiceBlock(choices=[
        ('full', 'Full Width'),
        ('half', 'Half Width'),
    ], default='full')

    text_alignment = TextAlignmentBlock(default='left')

    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = "streams/homepage_richtext_block.html"


class HighlightListBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120, help_text=_("Section title, max length 120 characters"))
    items_list = blocks.ListBlock(blocks.CharBlock(label=_("Item")))

    class Meta:
        template = "streams/highlight_list_block.html"
        icon = "tick"


class CaseStudyBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120, help_text=_(
        "Section title, max length 120 characters"))
    text_alignment = TextAlignmentBlock(default='left')
    content = blocks.RichTextBlock()

    button_text = blocks.CharBlock(max_length=120, required=False, help_text=_("Text for button"))
    button_link = blocks.PageChooserBlock()

    class Meta:
        template = "streams/case_study_block.html"
        icon = "image"


class DoOrDontCard(blocks.StructBlock):
    item = blocks.CharBlock(max_length=250, help_text=_("Item text"))


class DosAndDontsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, help_text=_("Do's and dont's title"))

    dos = blocks.ListBlock(
        DoOrDontCard()
    )

    donts = blocks.ListBlock(
        DoOrDontCard()
    )

    class Meta:
        template = "streams/do_dont_list.html"
        icon = "list-ul"
        label = "Do's and dont's"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(max_length=300, help_text=_("Quote"))
    attribution = blocks.CharBlock(max_length=120, help_text=_("Quote attribution"))

    class Meta:
        template = "streams/quote_block.html"


class CookieTableBlock(blocks.StructBlock):

    title = blocks.CharBlock(max_length=120, help_text=_("Section title, max length 120 characters"))
    content = blocks.RichTextBlock()
    table = TableBlock()

    class Meta:
        template = "streams/cookie_block.html"
        icon="table"


class LogoItem(blocks.StructBlock):
    logo = ImageChooserBlock(required=True, help_text=_("Logo of supporter"))
    url = blocks.URLBlock(max_length=250, help_text=_("URL of supporter"))
    logo_description = blocks.CharBlock(max_length=250, help_text=_("Alt description for the image"))


class SupportersBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, help_text=_("Do's and dont's title"))
    introduction = blocks.RichTextBlock()

    logos = blocks.ListBlock(
        LogoItem()
    )
    class Meta:
        template = "streams/supports_block.html"
        icon = "image"
        label = "Supporter logos"
