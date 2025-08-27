# milk/management/commands/delete_old_milk_history.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from milkhistory.models import MilkHistory


class Command(BaseCommand):
    help = "Deletes MilkHistory records older than 1 month"

    def handle(self, *args, **kwargs):
        one_month_ago = timezone.now() - timedelta(days=30)
        old_records = MilkHistory.objects.filter(created_at__lt=one_month_ago)
        count = old_records.count()
        old_records.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} old MilkHistory records"))
