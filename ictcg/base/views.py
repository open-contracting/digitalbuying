from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from health_check.views import MainView, MediaType
 
class HealthCheck(MainView):

    @never_cache
    def get(self, request, *args, **kwargs):
        status_code = 500 if self.errors else 200

        accept_header = request.META.get('HTTP_ACCEPT', '*/*')
        for media in MediaType.parse_header(accept_header):
            if media.mime_type in ('text/html', 'application/xhtml+xml', 'text/*', '*/*'):
                return HttpResponse('OK' if status_code == 200 else 'ERROR', status=status_code)

        return HttpResponse(
            'Not Acceptable: Supported content types: text/html, application/json',
            status=406,
            content_type='text/plain'
        )
