from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from reports.models import (
    ContinuationRow,
    CustomerSection,
    CustomerTotal,
    ParsedItem,
    ParsedReport,
    ReportTotal,
    UploadedReport,
)


class ParsedReportRetrievalAPITests(APITestCase):
    list_url = "/api/reports/"

    def _create_parsed_report(self, file_name, generated_date, generated_time):
        uploaded_report = UploadedReport.objects.create(file=f"reports/{file_name}")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date=generated_date,
            generated_time=generated_time,
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="100",
            total_in_prod="60",
            total_fatur="20",
            total_sdo="20",
            total_valor="1000,00",
        )
        return parsed_report

    def test_list_returns_200_and_empty_list_when_no_parsed_reports_exist(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_returns_reports_in_newest_first_order(self):
        older = self._create_parsed_report("older.txt", "06/04/2026", "10:00:00")
        newer = self._create_parsed_report("newer.txt", "07/04/2026", "11:00:00")

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], newer.id)
        self.assertEqual(response.data[1]["id"], older.id)

    def test_list_returns_top_level_fields_without_nested_customers_or_items(self):
        parsed_report = self._create_parsed_report("summary.txt", "06/04/2026", "15:55:47")

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="UTIMIL",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="4.000",
            total_in_prod="3.611",
            total_fatur="0",
            total_sdo="1.582",
            total_valor="31.649,460",
        )
        item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="402973",
            descricao="TIRA ZC",
        )
        ContinuationRow.objects.create(
            parsed_item=item,
            ord_prod="9.148.942",
            sit_ordem="LC10",
            qt_prod="1.172",
            sit="Em Produ",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data[0]
        self.assertEqual(result["uploaded_report_id"], parsed_report.uploaded_report_id)
        self.assertEqual(result["uploaded_file"], "reports/summary.txt")
        self.assertEqual(result["generated_date"], "06/04/2026")
        self.assertEqual(result["generated_time"], "15:55:47")
        self.assertIn("report_total", result)
        self.assertNotIn("customers", result)

    def test_detail_returns_full_nested_structure_for_existing_report(self):
        parsed_report = self._create_parsed_report("detail.txt", "06/04/2026", "15:55:47")

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="UTIMIL",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="4.000",
            total_in_prod="3.611",
            total_fatur="0",
            total_sdo="1.582",
            total_valor="31.649,460",
        )
        item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="402973",
            descricao="TIRA ZC",
            ord_prod="9.148.823",
            qt_prod="857",
            sit="Em Produ",
        )
        ContinuationRow.objects.create(
            parsed_item=item,
            ord_prod="9.148.942",
            sit_ordem="LC10",
            qt_prod="1.172",
            sit="Em Produ",
        )

        response = self.client.get(f"/api/reports/{parsed_report.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], parsed_report.id)
        self.assertEqual(response.data["uploaded_file"], "reports/detail.txt")
        self.assertIn("report_total", response.data)
        self.assertEqual(len(response.data["customers"]), 1)
        self.assertEqual(response.data["customers"][0]["customer_name"], "UTIMIL")
        self.assertEqual(response.data["customers"][0]["total"]["total_valor"], "31.649,460")
        self.assertEqual(response.data["customers"][0]["items"][0]["pedido"], "402973")
        self.assertEqual(
            response.data["customers"][0]["items"][0]["continuations"][0]["ord_prod"],
            "9.148.942",
        )

    def test_detail_returns_404_for_missing_report(self):
        response = self.client.get("/api/reports/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_returns_200_when_report_total_is_missing(self):
        uploaded_report = UploadedReport.objects.create(file="reports/no-total.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="06/04/2026",
            generated_time="15:55:47",
        )

        response = self.client.get(f"/api/reports/{parsed_report.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], parsed_report.id)
        self.assertIsNone(response.data["report_total"])
        self.assertEqual(response.data["customers"], [])


class ParsedReportListSerializerQueryTests(TestCase):
    def test_list_queryset_supports_report_total_without_customers(self):
        uploaded_report = UploadedReport.objects.create(file="reports/list-only.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="06/04/2026",
            generated_time="15:55:47",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="200",
            total_in_prod="100",
            total_fatur="50",
            total_sdo="50",
            total_valor="2000,00",
        )

        response = self.client.get("/api/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["report_total"]["total_ped"], "200")
