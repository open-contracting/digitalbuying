import os
from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views

urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^sitemap.xml/', sitemap),
    # url(r'^search/$', search_views.search, name='search'),
]

if os.getenv('BLOCK_SEARCH_ENGINES', 'off') == 'on':
    urlpatterns = [
        url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"))
    ] + urlpatterns

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar
    from django.views import defaults as default_views

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ] + urlpatterns

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),
]
