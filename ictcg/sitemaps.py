from django.db.models import Q
from wagtail.contrib.sitemaps import Sitemap
from wagtail.models import Page


class LocalisedSitemap(Sitemap):
    """
    A sitemap covering every locale's page tree.

    With Wagtail's i18n, each locale lives in its own page tree (the site's
    root_page and its translations). The default Wagtail sitemap only walks the
    site root_page's subtree, which would omit the non-default locales
    (e.g. /es/ and /id/). This includes all of them.
    """

    def items(self):
        site = self.get_wagtail_site()
        locale_roots = site.root_page.get_translations(inclusive=True)
        subtrees = Q()
        for root in locale_roots:
            subtrees |= Q(path__startswith=root.path)
        return Page.objects.filter(subtrees).live().public().order_by("path").defer_streamfields().specific()
