from django.http import JsonResponse
from .utils import handle_request_log

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
        if not ip_address:
            return JsonResponse({"error": "Forbidden"}, status=403)
        
        response = handle_request_log(ip_address="8.8.8.8", path=request.path)
        if response is None:
            response = self.get_response(request)
        
        """Code to be executed for each request/response after the view is called."""
        return response
     