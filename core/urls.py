# https://docs.wagtail.org/en/stable/advanced_topics/add_to_django_project.html#urls-py
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from core.sitemaps import LocalisedSitemap

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("sitemap.xml", sitemap, {"sitemaps": {"wagtail": LocalisedSitemap}}),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# Language-prefixed URLs (/en/, /es/, /id/). For anything not caught by a more
# specific rule above, hand over to Wagtail's serving mechanism.
# https://docs.wagtail.org/en/v2.15.6/advanced_topics/i18n.html
urlpatterns += i18n_patterns(
    re_path(r"", include(wagtail_urls)),
)
