import logging

from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable


class MainMenu(ClusterableModel):
    """MainMenu class for header links. Contains Orderable MenuItem class."""

    admin_title = models.CharField(max_length=100, blank=False, null=True)  # noqa: DJ001

    title = models.CharField(max_length=100)

    language = models.CharField(max_length=100, choices=settings.LANGUAGES)

    button_text = models.CharField(max_length=100, blank=False, null=False, default="Menu")

    button_aria_label = models.CharField(
        max_length=100,
        default="Show or hide Top Level Navigation",
        help_text="Description for navigation button aria label",
    )

    navigation_aria_label = models.CharField(
        max_length=100,
        default="Top Level Navigation",
        help_text="Description for navigation aria label",
    )

    phase_banner_description = RichTextField(
        blank=True,
        default="",
        help_text="Text area for phase banner description",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("language"),
        FieldPanel("button_text"),
        FieldPanel("button_aria_label"),
        FieldPanel("navigation_aria_label"),
        FieldPanel("phase_banner_description"),
        InlinePanel("menu_items", label="Menu Item"),
    ]

    def __str__(self):
        language = dict(settings.LANGUAGES)
        return f"{self.title} - {language[self.language]}"

    def save(self, *args, **kwargs):
        try:
            clear_mainmenu_cache(self.language)
        except Exception:
            logging.exception("Error deleting menu cache")
        return super().save(*args, **kwargs)


class MenuItem(models.Model):
    """Reuseable class for menu item links."""

    title = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        PageChooserPanel("page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.page:
            return self.page.url
        if self.url:
            return self.url
        return "#"


class MainMenuItem(Orderable, MenuItem):
    """
    A class that extends Orderable and MenuItem classe for the main menu link items.
    Extending Orderable allow for links to be arranaged in the order choosen by the user.
    """

    panels = [
        *MenuItem.panels,
    ]
    links = ParentalKey("MainMenu", related_name="menu_items")


class FooterMenu(ClusterableModel):
    """FooterMenu class for footer links. Contains Orderable MenuItem class."""

    admin_title = models.CharField(max_length=100, blank=False, null=True)  # noqa: DJ001

    language = models.CharField(max_length=100, choices=settings.LANGUAGES)

    quick_links_title = models.CharField(max_length=100, blank=False, null=True)  # noqa: DJ001

    sponsors_title = models.CharField(max_length=100, blank=False, null=True)  # noqa: DJ001

    translation_title = models.CharField(max_length=100, blank=False, null=True)  # noqa: DJ001

    panels = [
        FieldPanel("admin_title"),
        FieldPanel("language"),
        FieldPanel("quick_links_title"),
        FieldPanel("sponsors_title"),
        FieldPanel("translation_title"),
        InlinePanel("footer_menu_items", label="Menu Item"),
    ]

    def __str__(self):
        language = dict(settings.LANGUAGES)
        return f"{self.admin_title} - {language[self.language]}"

    def save(self, *args, **kwargs):
        try:
            clear_footer_cache(self.language)
        except Exception:
            logging.exception("Error deleting footer cache")
        return super().save(*args, **kwargs)


class FooterMenuItem(Orderable, MenuItem):
    """
    A class that extends Orderable and MenuItem classe for the main menu link items.
    Extending Orderable allow for links to be arranaged in the order choosen by the user.
    """

    panels = [
        *MenuItem.panels,
    ]
    links = ParentalKey("FooterMenu", related_name="footer_menu_items")


def clear_mainmenu_cache(language_code):
    navigation_links = make_template_fragment_key("header_navigation_links", [language_code])
    cache.delete(navigation_links)


def clear_footer_cache(language_code):
    support_link = make_template_fragment_key("footer_support_links", [language_code])
    cache.delete_many([support_link])


@receiver(pre_delete, sender=MainMenu)
def on_main_menu_delete(sender, instance, **kwargs):  # noqa: ARG001
    """On main menu delete, clear the cache."""
    clear_mainmenu_cache(instance.language)


@receiver(pre_delete, sender=FooterMenu)
def on_footer_menu_delete(sender, instance, **kwargs):  # noqa: ARG001
    """On footer menu delete, clear the cache."""
    clear_footer_cache(instance.language)
