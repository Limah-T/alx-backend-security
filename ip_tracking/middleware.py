from .models import RequestLog, BlockedIP
from django.core.exceptions import PermissionDenied
import datetime

class CustomIpTrackingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response
    
    def __call__(self, request):
        """Code to be executed for each request before the view (and later middleware) are called."""
        # Safely extract IP address (supports proxies)
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()  # First IP in list
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        path = request.path
        date = datetime.datetime.today()
        if not ip_address:
            raise PermissionDenied
        log = RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=date)
        if BlockedIP.objects.filter(request_log=log.ip_address).exists():
            raise PermissionDenied
        response = self.get_response(request)

        """Code to be executed for each request/response after the view is called."""
        return response