from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from reports.models import UploadedReport


@override_settings(MEDIA_ROOT="/tmp/srp_test_media")
class ReportUploadAPITests(APITestCase):
    """
    Test suite for the SRP upload endpoint.

    Purpose:
        Verify that the upload API accepts supported file types,
        rejects unsupported requests, and persists UploadedReport
        records correctly.

    Covered behaviors:
        - valid TXT upload returns 201
        - valid PDF upload returns 201
        - missing file returns 400
        - invalid file type returns 400

    Notes:
        - tests use small in-memory files via SimpleUploadedFile
        - validation is extension-based only, per current MVP scope
        - authentication is not part of SRP MVP upload flow
    """

    upload_url = "/api/reports/upload/"

    def test_upload_txt_file_returns_201_and_creates_record(self):
        """
        Ensure a valid TXT file upload succeeds and creates an UploadedReport.
        """
        txt_file = SimpleUploadedFile(
            name="sample_report.txt",
            content=b"order: 123\nclient: ACME\nstatus: pending\n",
            content_type="text/plain",
        )

        response = self.client.post(
            self.upload_url,
            {"file": txt_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedReport.objects.count(), 1)

        report = UploadedReport.objects.first()
        self.assertIsNotNone(report)
        self.assertTrue(report.file.name.endswith(".txt"))

        self.assertIn("id", response.data)
        self.assertIn("file", response.data)
        self.assertIn("uploaded_at", response.data)
        self.assertEqual(response.data["message"], "File uploaded successfully.")

    def test_upload_pdf_file_returns_201_and_creates_record(self):
        """
        Ensure a valid PDF file upload succeeds and creates an UploadedReport.
        """
        pdf_file = SimpleUploadedFile(
            name="sample_report.pdf",
            content=b"%PDF-1.4 test pdf content",
            content_type="application/pdf",
        )

        response = self.client.post(
            self.upload_url,
            {"file": pdf_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedReport.objects.count(), 1)

        report = UploadedReport.objects.first()
        self.assertIsNotNone(report)
        self.assertTrue(report.file.name.endswith(".pdf"))

        self.assertIn("id", response.data)
        self.assertIn("file", response.data)
        self.assertIn("uploaded_at", response.data)
        self.assertEqual(response.data["message"], "File uploaded successfully.")

    def test_upload_without_file_returns_400(self):
        """
        Ensure the endpoint rejects requests that do not include a file.
        """
        response = self.client.post(
            self.upload_url,
            {},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No file provided.")
        self.assertEqual(UploadedReport.objects.count(), 0)

    def test_upload_invalid_file_type_returns_400(self):
        """
        Ensure unsupported file extensions are rejected.
        """
        csv_file = SimpleUploadedFile(
            name="sample_report.csv",
            content=b"order,client,status\n123,ACME,pending\n",
            content_type="text/csv",
        )

        response = self.client.post(
            self.upload_url,
            {"file": csv_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Unsupported file type. Only .txt and .pdf files are allowed.",
        )
        self.assertEqual(UploadedReport.objects.count(), 0)