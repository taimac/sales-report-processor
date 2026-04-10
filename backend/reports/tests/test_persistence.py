from django.test import TestCase
from reports.models import UploadedReport, ParsedReport
from reports.services.report_persistence import persist_report


class ReportPersistenceTests(TestCase):
    def test_persist_report_creates_full_structure(self):
        uploaded = UploadedReport.objects.create(
            file="reports/carteira_06_04_26.txt"
        )

        parsed = persist_report(uploaded)

        self.assertIsInstance(parsed, ParsedReport)
        self.assertTrue(parsed.customers.exists())
        self.assertTrue(parsed.total)