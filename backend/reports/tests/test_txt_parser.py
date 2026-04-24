from pathlib import Path

from django.test import SimpleTestCase

from reports.services.txt_parser import ( 
    extract_generated_datetime, 
    read_txt_report, 
    classify_line, 
    classify_report_lines, 
    detect_customer_blocks,
    _extract_primary_status,
    parse_main_detail_lines,
    parse_main_row_identity_fields,
    parse_main_row_full_step_1,
    parse_main_row_full,
    attach_continuation_rows,
    extract_totals,
    assemble_report
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

    def test_parse_main_row_identity_fields_keeps_three_digit_seq(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  402258    150 TIRA FF BOB 0,60 SAE1006 OL")
        )

        parsed = parse_main_row_identity_fields(line)

        self.assertEqual(parsed["pedido"], "402258")
        self.assertEqual(parsed["seq"], "150")

    def test_parse_main_row_full_keeps_three_digit_seq(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  402258    200 TIRA FF BOB 0,60 SAE1006 OL")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["pedido"], "402258")
        self.assertEqual(parsed["seq"], "200")

    def test_parse_main_detail_lines_returns_only_main_rows(self) -> None:
        parsed_rows = parse_main_detail_lines(self.data["lines"])

        self.assertGreater(len(parsed_rows), 0)
        self.assertTrue(all("raw_line" in row for row in parsed_rows))
        self.assertTrue(all(row["est"] for row in parsed_rows))


class TxtParserOperationalTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = (
            Path(__file__).resolve().parents[2]
            / "media/reports/carteira_06_04_26.txt"
        )
        self.data = read_txt_report(self.sample_path)

    def test_parse_operational_fields_for_gpaniz(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  404565     10 CHAPA ZC 0,50")
        )

        parsed = parse_main_row_full_step_1(line)

        self.assertEqual(parsed["compr"], "2580")
        self.assertEqual(parsed["ord_prod"], "9.154.169")
        self.assertEqual(parsed["dt_entr"], "13/04/26")
        self.assertEqual(parsed["aa"], "Nao")
        self.assertEqual(parsed["qt_ped"], "1.500")
        self.assertEqual(parsed["qt_prod"], "0")
        self.assertEqual(parsed["sdo_estoq"], "1.454")
        self.assertTrue(parsed["sit"])

    def test_extract_primary_status_keeps_known_multiword_statuses(self) -> None:
        self.assertEqual(_extract_primary_status("Fat Parc      9,290 0,000 435"), "Fat Parc")
        self.assertEqual(_extract_primary_status("Em Produ      8,870 0,000 350"), "Em Produ")
        self.assertEqual(_extract_primary_status("OP Cancel     7,740 0,000 612"), "OP Cancel")
        self.assertEqual(_extract_primary_status("Sem MP        5,250 0,000 612"), "Sem MP")

    def test_parse_operational_fields_normalizes_status_at_parse_time(self) -> None:
        flantech_line = next(
            l for l in self.data["lines"]
            if l.startswith("11  400396     10 TIRA ZC BOB 1,25 NBR7008 ZC CR MI REV")
        )
        gpaniz_line = next(
            l for l in self.data["lines"]
            if l.startswith("11  404565     10 CHAPA ZC 0,50")
        )
        utimil_line = next(
            l for l in self.data["lines"]
            if l.startswith("11  402973     10 TIRA ZC BOB 0,95 NBR7008 ZC CR NO REV")
        )

        self.assertEqual(parse_main_row_full_step_1(flantech_line)["sit"], "Fat Parc")
        self.assertEqual(parse_main_row_full_step_1(gpaniz_line)["sit"], "OP Cancel")
        self.assertEqual(parse_main_row_full_step_1(utimil_line)["sit"], "Em Produ")

    def test_parse_operational_fields_when_ord_prod_is_blank(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  404521     30 TIRA ZC BOB 1,25 NBR7008 ZC CR MI REV")
        )

        parsed = parse_main_row_full_step_1(line)

        self.assertEqual(parsed["ord_prod"], "")
        self.assertEqual(parsed["sit_ordem"], "")
        self.assertEqual(parsed["dt_entr"], "06/04/26")
        self.assertEqual(parsed["aa"], "Nao")
        self.assertEqual(parsed["qt_ped"], "500")
        self.assertEqual(parsed["qt_pc"], "0")
        self.assertEqual(parsed["qt_prod"], "0")
        self.assertEqual(parsed["qt_fatur"], "0")
        self.assertEqual(parsed["sdo_estoq"], "0")
        self.assertEqual(parsed["sit"], "Planejmto")

class TxtParserCommercialTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = (
            Path(__file__).resolve().parents[2]
            / "media/reports/carteira_06_04_26.txt"
        )
        self.data = read_txt_report(self.sample_path)

    def test_parse_commercial_fields_gpaniz(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  404565     10 CHAPA ZC 0,50")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["pre_liq"], "3,740")
        self.assertEqual(parsed["pf"], "0,000")
        self.assertEqual(parsed["pag"], "612")
        self.assertEqual(parsed["transp"], "A�OLOG-RS")
        self.assertEqual(parsed["cr_pro"], "Sim")
        self.assertEqual(parsed["cr_fat"], "Sim")
        self.assertEqual(parsed["o_compra"], "208575")

    def test_parse_commercial_fields_handles_two_token_transporter(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  402254     40 CHAPA GR LTQ  8,00 NBR 6656 LNE 38")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["transp"], "RETIRA RS")
        self.assertEqual(parsed["cr_pro"], "Sim")
        self.assertEqual(parsed["cr_fat"], "Sim")
        self.assertEqual(parsed["o_compra"], "319655")
        self.assertEqual(parsed["sit"], "Produzido")

    def test_parse_commercial_fields_preserves_sem_mp_status(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  404651     20 CHAPA FQ 2,65 NBR6658")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["sit"], "Sem MP")
        self.assertEqual(parsed["transp"], "A�OLOG-RS")
        self.assertEqual(parsed["cr_pro"], "Sim")
        self.assertEqual(parsed["cr_fat"], "Sim")

    def test_parse_commercial_fields_handles_missing_o_compra_with_two_numeric_refs(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  402150     10 TIRA FQ DEC BOB 2,25 NBR6658 OL")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["transp"], "A�OLOG-RS")
        self.assertEqual(parsed["cr_pro"], "Sim")
        self.assertEqual(parsed["cr_fat"], "Sim")
        self.assertEqual(parsed["o_compra"], "")
        self.assertEqual(parsed["item_cli"], "20013")
        self.assertEqual(parsed["mnf"], "4")

    def test_parse_commercial_fields_treats_two_full_numeric_refs_as_o_compra_and_item_cli(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  400569     60 TIRA ZC BOB 1,95 NBR7008 ZC CR MI RV Z")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["o_compra"], "17369")
        self.assertEqual(parsed["item_cli"], "20005")
        self.assertEqual(parsed["mnf"], "")

    def test_parse_commercial_fields_keeps_cfe_email_as_single_purchase_order(self) -> None:
        line = next(
            l for l in self.data["lines"]
            if l.startswith("11  403827     20 TIRA ZC BOB 1,25 NBR7008 ZC CR MI REV")
        )

        parsed = parse_main_row_full(line)

        self.assertEqual(parsed["o_compra"], "cfe email")
        self.assertEqual(parsed["item_cli"], "")
        self.assertEqual(parsed["mnf"], "")

from reports.services.txt_parser import attach_continuation_rows


class TxtParserContinuationTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = (
            Path(__file__).resolve().parents[2]
            / "media/reports/carteira_06_04_26.txt"
        )
        self.data = read_txt_report(self.sample_path)

    def test_continuation_rows_attached_with_expected_fields(self) -> None:
        rows = attach_continuation_rows(self.data["lines"])

        row = next(r for r in rows if r["continuations"])
        continuation = row["continuations"][0]

        self.assertIn("ord_prod", continuation)
        self.assertIn("sit_ordem", continuation)
        self.assertIn("qt_prod", continuation)
        self.assertIn("sit", continuation)

        self.assertTrue(continuation["ord_prod"])
        self.assertTrue(continuation["sit"])


class TxtParserTotalsTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = (
            Path(__file__).resolve().parents[2]
            / "media/reports/carteira_06_04_26.txt"
        )
        self.data = read_txt_report(self.sample_path)

    def test_extract_totals(self) -> None:
        totals = extract_totals(self.data["lines"])

        self.assertTrue(totals["client_totals"])
        self.assertTrue(totals["grand_totals"])

        first_client = totals["client_totals"][0]

        self.assertIn("total_ped", first_client)
        self.assertIn("total_sdo", first_client)

    def test_extract_client_totals_values(self):
        totals = extract_totals(self.data["lines"])

        first_client = totals["client_totals"][0]

        self.assertEqual(first_client["total_ped"], "71.500")
        self.assertEqual(first_client["total_in_prod"], "92.679")
        self.assertEqual(first_client["total_fatur"], "32.196")
        self.assertEqual(first_client["total_sdo"], "31.903")

    def test_extract_grand_totals(self):
        totals = extract_totals(self.data["lines"])

        grand = totals["grand_totals"][0]

        self.assertEqual(grand["total_ped"], "292.850")
        self.assertEqual(grand["total_in_prod"], "157.851")
        self.assertEqual(grand["total_fatur"], "36.279")
        self.assertEqual(grand["total_sdo"], "72.454")

    def test_extract_grand_total_currency(self):
        totals = extract_totals(self.data["lines"])

        grand = totals["grand_totals"][0]

        self.assertIn("total_valor", grand)
        self.assertEqual(grand["total_valor"], "2.078.254,440")

class TxtParserFinalAssemblyTests(SimpleTestCase):
    def setUp(self) -> None:
        self.sample_path = (
            Path(__file__).resolve().parents[2]
            / "media/reports/carteira_06_04_26.txt"
        )

    def test_full_report_structure(self) -> None:
        report = assemble_report(self.sample_path)

        self.assertIn("metadata", report)
        self.assertIn("customers", report)
        self.assertIn("totals", report)
        self.assertIn("grand_totals", report["totals"])

        self.assertTrue(report["customers"])
        self.assertTrue(report["totals"]["grand_totals"])

        first_customer = report["customers"][0]

        self.assertIn("representative", first_customer)
        self.assertIn("customer_name", first_customer)
        self.assertIn("items", first_customer)
        self.assertIn("totals", first_customer)
        self.assertIn("client_totals", first_customer["totals"])

        self.assertTrue(first_customer["items"])
