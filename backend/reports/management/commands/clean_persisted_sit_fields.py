"""
Purpose: Clean legacy ParsedItem status values persisted before parser normalization.
Date: 2026-04-14
Author: Codex
Domain: Systems / SRP
"""

from django.core.management.base import BaseCommand

from reports.models import ParsedItem
from reports.services.txt_parser import _extract_primary_status


class Command(BaseCommand):
    help = "Clean corrupted 'sit' fields in persisted ParsedItem records."

    def handle(self, *args, **options):
        processed_count = 0
        updated_count = 0

        for item in ParsedItem.objects.all():
            processed_count += 1
            cleaned_status = _extract_primary_status(item.sit)
            if cleaned_status != item.sit:
                item.sit = cleaned_status
                item.save(update_fields=["sit"])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed {processed_count} items. Cleaned {updated_count} corrupted 'sit' fields."
            )
        )
