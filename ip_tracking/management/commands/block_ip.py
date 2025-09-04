from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import RequestLog, BlockedIP
from django.db.models import Count
from django.utils import timezone

class Command(BaseCommand):
    help = "Adds IP address to BlockedIp Model"

    def handle(self, *args, **options): 
        time_stamp = timezone.now() - timezone.timedelta(minutes=2) 
        suspicious_ids = (RequestLog.objects.filter(timestamp__gte=time_stamp).values("ip_address").annotate(request_count=Count('id')).filter(request_count__gt=2))
        if suspicious_ids:
            for block_id in suspicious_ids:
                log = block_id['request_log']
                ip_address = block_id['ip_address']
                ip_addr=BlockedIP.objects.get_or_create(request_log=log, ip_address=ip_address)
                self.stdout.write(self.style.SUCCESS(f"IP address: {ip_addr.ip_address} has been blocked!"))
        else:
            self.stdout.write(self.style.ERROR("Oops!"))
            pass