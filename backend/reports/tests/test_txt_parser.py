from pathlib import Path

from django.test import SimpleTestCase

from reports.services.txt_parser import extract_generated_datetime, read_txt_report


class TxtParserReaderTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = Path(__file__).resolve().parents[2] / "media/reports/carteira_06_04_26.txt"

    def test_read_txt_report_returns_raw_text_lines_and_metadata(self) -> None:
        result = read_txt_report(self.sample_path)

        self.assertIn("raw_text", result)
        self.assertIn("lines", result)
        self.assertIn("metadata", result)

        self.assertTrue(result["raw_text"])
        self.assertGreater(len(result["lines"]), 0)

    def test_extract_generated_datetime_from_real_sample(self) -> None:
        result = read_txt_report(self.sample_path)

        self.assertEqual(result["metadata"]["generated_date"], "06/04/2026")
        self.assertEqual(result["metadata"]["generated_time"], "15:55:47")

    def test_extract_generated_datetime_returns_none_when_missing(self) -> None:
        metadata = extract_generated_datetime(["header line", "another line"])

        self.assertIsNone(metadata["generated_date"])
        self.assertIsNone(metadata["generated_time"])