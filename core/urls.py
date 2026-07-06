# https://docs.wagtail.org/en/stable/advanced_topics/add_to_django_project.html#urls-py
import re

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve
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
# https://docs.wagtail.org/en/stable/advanced_topics/i18n.html
urlpatterns += i18n_patterns(path("", include(wagtail_urls)))

if settings.SERVE_STATIC:
    # Emulate static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # https://github.com/django/django/blob/stable/5.2.x/django/conf/urls/static.py
    urlpatterns += [
        re_path(
            rf"^{re.escape(settings.STATIC_URL.lstrip('/'))}(?P<path>.*)$",
            serve,
            {"document_root": settings.STATIC_ROOT},
        ),
    ]
