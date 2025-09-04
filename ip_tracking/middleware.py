from .models import RequestLog, BlockedIP
from django.core.exceptions import PermissionDenied
import datetime, requests, os

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
        API_KEY = os.environ.get("IPGEOLOCATION_IO_API_KEY")
        # IP_ADDR = ip_address
        URL = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={API_KEY}&ip=8.8.8.8&fields=location.country_name,location.city"
        headers = {}
        request_ip_geo = requests.get(url=URL, headers=headers, data={})
        data = request_ip_geo.json()
        print(data)

        log = RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=date, country=data['location']['country_name'].title(), city=data['location']['city'].title())

        if BlockedIP.objects.filter(request_log=log).exists():
            raise PermissionDenied
        response = self.get_response(request)

        """Code to be executed for each request/response after the view is called."""
        return response