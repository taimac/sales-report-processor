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
            customer_name="Multimil",
        )

        self.assertEqual(customer.parsed_report, parsed)
        self.assertEqual(customer.customer_name, "Multimil")
        self.assertEqual(customer.representative, "JOAO")

from reports.models import ParsedItem


class ParsedItemModelTests(TestCase):
    def test_create_parsed_item(self):
        uploaded = UploadedReport.objects.create(file="reports/test.txt")

        parsed = ParsedReport.objects.create(
            uploaded_report=uploaded,
            generated_date="06/04/26",
            generated_time="18:30",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed,
            representative="JOAO",
            customer_name="Multimil",
        )

        item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="12345",
            descricao="CHAPA ZC",
        )

        self.assertEqual(item.customer_section, customer)
        self.assertEqual(item.pedido, "12345")

from reports.models import ContinuationRow


class ContinuationRowModelTests(TestCase):
    def test_create_continuation_row(self):
        uploaded = UploadedReport.objects.create(file="reports/test.txt")

        parsed = ParsedReport.objects.create(
            uploaded_report=uploaded,
            generated_date="06/04/26",
            generated_time="18:30",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed,
            representative="JOAO",
            customer_name="Multimil",
        )

        item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="12345",
        )

        continuation = ContinuationRow.objects.create(
            parsed_item=item,
            ord_prod="9.154.040",
            sit_ordem="LC10",
            qt_prod="1000",
            sit="Fat Parc",
        )

        self.assertEqual(continuation.parsed_item, item)
        self.assertEqual(continuation.ord_prod, "9.154.040")

from reports.models import CustomerTotal, ReportTotal


class TotalsModelTests(TestCase):
    def test_create_totals(self):
        uploaded = UploadedReport.objects.create(file="reports/test.txt")

        parsed = ParsedReport.objects.create(
            uploaded_report=uploaded,
            generated_date="06/04/26",
            generated_time="18:30",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed,
            representative="JOAO",
            customer_name="Multimil",
        )

        customer_total = CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="1000",
            total_valor="50000",
        )

        report_total = ReportTotal.objects.create(
            parsed_report=parsed,
            total_ped="5000",
            total_valor="250000",
        )

        self.assertEqual(customer_total.customer_section, customer)
        self.assertEqual(report_total.parsed_report, parsed)