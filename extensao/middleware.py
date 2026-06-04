from django.middleware.csrf import CsrfViewMiddleware


class ApiCsrfExemptMiddleware(CsrfViewMiddleware):
    """Skips all CSRF checks for /extensao/api/ routes.

    Necessary because Chrome extensions send Origin: chrome-extension://...
    which Django 6.x rejects in process_request() before csrf_exempt is checked.
    API routes use Token authentication and don't need CSRF protection.
    """

    def process_request(self, request):
        if request.path.startswith('/extensao/api/'):
            request.csrf_processing_done = True
            return
        super().process_request(request)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith('/extensao/api/'):
            return None
        return super().process_view(request, callback, callback_args, callback_kwargs)
