from csv import DictReader
from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from reports.services.csv_exporter import export_report_to_csv


class CsvExporterTests(SimpleTestCase):
    def test_export_report_to_csv_writes_continuations_as_separate_rows(self) -> None:
        report = {
            "customers": [
                {
                    "representative": "MACIEL",
                    "customer_name": "METALMATRIX",
                    "items": [
                        {
                            "est": "11",
                            "pedido": "400569",
                            "seq": "60",
                            "descricao": "TIRA FQ DEC BOB 2,25 NBR6658 OL",
                            "espess": "2,25",
                            "larg": "90,00",
                            "compr": "0",
                            "ord_prod": "9.147.642",
                            "sit_ordem": "",
                            "dt_entr": "13/04/26",
                            "aa": "Nao",
                            "qt_ped": "10",
                            "qt_pc": "0",
                            "qt_prod": "1.018",
                            "qt_fatur": "0",
                            "sdo_estoq": "9.998",
                            "sit": "Produzido",
                            "pre_liq": "6,850",
                            "pf": "0,000",
                            "vlr_peca": "",
                            "pag": "426",
                            "transp": "A\u00C7OLOG-RS",
                            "cr_pro": "Sim",
                            "cr_fat": "Sim",
                            "o_compra": "",
                            "item_cli": "17369",
                            "mnf": "20005",
                            "raw_line": "main row",
                            "continuations": [
                                {
                                    "ord_prod": "9.147.700",
                                    "sit_ordem": "LC12",
                                    "qt_prod": "250",
                                    "sit": "Em Produ",
                                    "raw_line": "continuation row",
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.csv"

            export_report_to_csv(report, output_path)

            with output_path.open("r", encoding="utf-8", newline="") as csvfile:
                rows = list(DictReader(csvfile, delimiter=";"))

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["pedido"], "400569")
        self.assertEqual(rows[0]["ord_prod"], "9.147.642")
        self.assertEqual(rows[0]["qt_ped"], "10.000")
        self.assertEqual(rows[0]["qt_prod"], "1.018")
        self.assertEqual(rows[0]["sit"], "Produzido")

        self.assertEqual(rows[1]["pedido"], "400569")
        self.assertEqual(rows[1]["seq"], "60")
        self.assertEqual(rows[1]["ord_prod"], "9.147.700")
        self.assertEqual(rows[1]["sit_ordem"], "LC12")
        self.assertEqual(rows[1]["qt_prod"], "250")
        self.assertEqual(rows[1]["sit"], "Em Produ")
        self.assertEqual(rows[1]["o_compra"], "")
        self.assertEqual(rows[1]["item_cli"], "17369")
        self.assertEqual(rows[1]["mnf"], "20005")
