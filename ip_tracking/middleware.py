from .models import RequestLog
import datetime

class CustomIpTrackingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response
    
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        date = datetime.datetime.today()
        if ip_address and path:
            RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=date)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response