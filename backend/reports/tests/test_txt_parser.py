from pathlib import Path

from django.test import SimpleTestCase

from reports.services.txt_parser import ( 
    extract_generated_datetime, 
    read_txt_report, 
    classify_line, 
    classify_report_lines, 
    detect_customer_blocks,
    parse_main_detail_lines,
    parse_main_row_identity_fields
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


class TxtParserMainRowParsingTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = (
            Path(__file__).resolve().parents[2]
            / "media/reports/carteira_06_04_26.txt"
        )
        self.data = read_txt_report(self.sample_path)

    def test_parse_main_row_identity_fields_for_gpaniz_row(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  404565     10 CHAPA ZC 0,50 NBR7008 ZC CR NO RV Z275")
        )

        parsed = parse_main_row_identity_fields(line)

        self.assertEqual(parsed["est"], "11")
        self.assertEqual(parsed["pedido"], "404565")
        self.assertEqual(parsed["seq"], "10")
        self.assertEqual(
            parsed["descricao"],
            "CHAPA ZC 0,50 NBR7008 ZC CR NO RV Z275",
        )
        self.assertEqual(parsed["espess"], "0,50")
        self.assertEqual(parsed["larg"], "1.000,00")
        self.assertEqual(parsed["compr"], "2580")

    def test_parse_main_row_identity_fields_for_flantech_row_with_blank_compr(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  400396     10 TIRA ZC BOB 1,25 NBR7008 ZC CR MI REV")
        )

        parsed = parse_main_row_identity_fields(line)

        self.assertEqual(parsed["est"], "11")
        self.assertEqual(parsed["pedido"], "400396")
        self.assertEqual(parsed["seq"], "10")
        self.assertEqual(
            parsed["descricao"],
            "TIRA ZC BOB 1,25 NBR7008 ZC CR MI REV",
        )
        self.assertEqual(parsed["espess"], "1,25")
        self.assertEqual(parsed["larg"], "23,50")
        self.assertEqual(parsed["compr"], "0")

    def test_parse_main_detail_lines_returns_only_main_rows(self) -> None:
        parsed_rows = parse_main_detail_lines(self.data["lines"])

        self.assertGreater(len(parsed_rows), 0)
        self.assertTrue(all("raw_line" in row for row in parsed_rows))
        self.assertTrue(all(row["est"] for row in parsed_rows))