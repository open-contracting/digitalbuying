from django.utils.html import format_html, mark_safe
from wagtail.images.formats import Format, register_image_format


class CaptionedImageFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):
        default_html = super().image_to_html(image, "", extra_attributes)
        return format_html("<figure>{}<figcaption>{}</figcaption></figure>", default_html, mark_safe(alt_text))


register_image_format(
    CaptionedImageFormat("captioned_fullwidth", "Full width captioned", "richtext-image full-width", "width-800")
)
