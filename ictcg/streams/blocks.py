from wagtail.core import blocks
from django.utils.translation import ugettext_lazy as _

class RichTextWithTitleBlock(blocks.StructBlock):
  title = blocks.CharBlock(max_length=120, help_text=_("Section title, max length 120 characters"))
  content = blocks.RichTextBlock()

  class Meta:
    template="streams/richtext_block.html"


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
    template="streams/do_dont_list.html"
    icon="list-ul"
    label="Do's and dont's"
  
class QuoteBlock(blocks.StructBlock):
  title = blocks.CharBlock(max_length=120, help_text=_("Quote section title, max length 120 characters"))
  content_top = blocks.RichTextBlock()
  quote = blocks.CharBlock(max_length=300, help_text=_("Quote"))
  attribution = blocks.CharBlock(max_length=120, help_text=_("Quote attribution"))
  content_bottom = blocks.RichTextBlock()

  class Meta:
    template="streams/quote_block.html"
