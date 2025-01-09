# https://docs.wagtail.org/en/stable/advanced_topics/add_to_django_project.html#urls-py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("sitemap.xml", sitemap),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r"", include(wagtail_urls)),
]
