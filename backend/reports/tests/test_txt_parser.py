from pathlib import Path

from django.test import SimpleTestCase

from reports.services.txt_parser import ( 
    extract_generated_datetime, 
    read_txt_report, 
    classify_line, 
    classify_report_lines, 
    detect_customer_blocks
)


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

class TxtParserClassificationTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = Path(__file__).resolve().parents[2] / "media/reports/carteira_06_04_26.txt"
        self.data = read_txt_report(self.sample_path)

    def test_classify_known_line_types(self) -> None:
        lines = self.data["lines"]

        # pick representative samples
        customer_line = next(l for l in lines if "Rep:" in l and "Cliente:" in l)
        total_line = next(l for l in lines if "TOT CLIENTE:" in l)
        grand_total_line = next(l for l in lines if "TOTAL GERAL:" in l)

        self.assertEqual(classify_line(customer_line), "customer_header")
        self.assertEqual(classify_line(total_line), "client_total")
        self.assertEqual(classify_line(grand_total_line), "grand_total")

    def test_classify_report_lines_output_shape(self) -> None:
        classified = classify_report_lines(self.data["lines"])

        self.assertIsInstance(classified, list)
        self.assertIn("line", classified[0])
        self.assertIn("type", classified[0])

    def test_detect_customer_blocks(self) -> None:
        blocks = detect_customer_blocks(self.data["lines"])

        self.assertGreater(len(blocks), 0)

        first_block = blocks[0]

        self.assertIn("representative", first_block)
        self.assertIn("customer_name", first_block)
        self.assertIn("lines", first_block)

        self.assertTrue(first_block["customer_name"])