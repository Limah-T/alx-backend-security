from .models import RequestLog, BlockedIP
from django.utils import timezone
from django.http import JsonResponse
import requests, os

def handle_ipgeolocation(ip_address):
    API_KEY = os.environ.get("IPGEOLOCATION_IO_API_KEY")
    URL = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={API_KEY}&ip={ip_address}&fields=location.country_name,location.city"

    headers = {}
    try:
        request_ip_geo = requests.get(url=URL, headers=headers, data={})
        data = request_ip_geo.json()
    except Exception:
        pass
    return data

def handle_request_log(ip_address, path):
    data = handle_ipgeolocation(ip_address=ip_address)
    country = data.get("location", {}).get("country_name", "Unknown")
    city = data.get("location", {}).get("city", "Unknown")
    print(country, city)
    RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=timezone.now(), country=country.title(), city=city.title())

    """Check if IP has been blocked before allowing requests"""
    if BlockedIP.objects.filter(ip_address=ip_address).exists():
        return JsonResponse({"error": "Forbidden"}, status=403)
    return None