from django.test import TestCase
from reports.models import ParsedReport, UploadedReport, CustomerSection


class ParsedReportModelTests(TestCase):
    def test_create_parsed_report(self):
        uploaded = UploadedReport.objects.create(
            file="reports/test.txt"
        )

        parsed = ParsedReport.objects.create(
            uploaded_report=uploaded,
            generated_date="06/04/26",
            generated_time="18:30",
        )

        self.assertEqual(parsed.uploaded_report, uploaded)
        self.assertEqual(parsed.generated_date, "06/04/26")
        self.assertEqual(parsed.generated_time, "18:30")

class CustomerSectionModelTests(TestCase):
    def test_create_customer_section(self):
        uploaded = UploadedReport.objects.create(file="reports/test.txt")

        parsed = ParsedReport.objects.create(
            uploaded_report=uploaded,
            generated_date="06/04/26",
            generated_time="18:30",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed,
            representative="JOAO",
            customer_name="G PANIZ",
        )

        self.assertEqual(customer.parsed_report, parsed)
        self.assertEqual(customer.customer_name, "G PANIZ")
        self.assertEqual(customer.representative, "JOAO")