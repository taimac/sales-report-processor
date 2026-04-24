from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from reports.models import CustomerSection, ParsedItem, ParsedReport, UploadedReport


class CleanPersistedSitFieldsCommandTests(TestCase):
    def test_clean_persisted_sit_fields_normalizes_legacy_status_values(self):
        uploaded_report = UploadedReport.objects.create(file="reports/legacy-status.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="14/04/2026",
            generated_time="10:00:00",
        )
        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="LEGACY",
        )
        corrupted_item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="500001",
            seq="10",
            descricao="ITEM CORROMPIDO",
            sit="Fat Parc 9,290 0,000 435 VELOZ Sim Nao 6710",
        )
        clean_item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="500002",
            seq="20",
            descricao="ITEM LIMPO",
            sit="Produzido",
        )

        stdout = StringIO()
        call_command("clean_persisted_sit_fields", stdout=stdout)

        corrupted_item.refresh_from_db()
        clean_item.refresh_from_db()

        self.assertEqual(corrupted_item.sit, "Fat Parc")
        self.assertEqual(clean_item.sit, "Produzido")
        self.assertIn("Processed 2 items. Cleaned 1 corrupted 'sit' fields.", stdout.getvalue())
