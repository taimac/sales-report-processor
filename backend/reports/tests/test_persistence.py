from django.test import TestCase
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from unittest.mock import patch
from reports.models import UploadedReport, ParsedReport, CustomerSection, ParsedItem, ContinuationRow, CustomerTotal, ReportTotal
from reports.services.report_persistence import (
    ReportProcessingError,
    persist_report,
)


class ReportPersistenceTests(TestCase):
    """
    Tests for persisting parsed TXT report data into database models.
    Validates full flow from parser output to saved models.
    """

    def setUp(self):
        """Set up test data with a sample uploaded report."""
        self.uploaded_report = UploadedReport.objects.create(
            file=ContentFile("Sample TXT content", name="sample.txt")
        )

    def test_persist_report_with_real_parser(self):
        uploaded = UploadedReport.objects.create(
            file="reports/carteira_06_04_26.txt"
        )

        parsed = persist_report(uploaded)

        self.assertEqual(parsed.generated_date, "06/04/2026")
        self.assertEqual(parsed.generated_time, "15:55:47")

        self.assertTrue(parsed.customers.exists())

        customer = CustomerSection.objects.get(
            parsed_report=parsed,
            customer_name="CHAPAPLANA",
        )
        self.assertEqual(customer.representative, "Marcos")

        item = ParsedItem.objects.get(
            customer_section=customer,
            pedido="400396",
        )
        self.assertEqual(item.seq, "10")
        self.assertEqual(item.descricao, "TIRA ZC BOB 1,25 NBR7008 ZC CR MI REV")
        self.assertEqual(item.ord_prod, "9.139.943")
        self.assertEqual(item.qt_ped, "12.000")
        self.assertEqual(item.qt_prod, "8.386")
        self.assertEqual(item.sit, "Fat Parc")

        continuation = ContinuationRow.objects.filter(parsed_item=item).order_by("id").first()
        self.assertIsNotNone(continuation)
        self.assertEqual(continuation.ord_prod, "9.139.944")
        self.assertEqual(continuation.qt_prod, "4.148")
        self.assertEqual(continuation.sit, "Fat Parc")

        customer_total = CustomerTotal.objects.get(customer_section=customer)
        self.assertEqual(customer_total.total_ped, "71.500")
        self.assertEqual(customer_total.total_in_prod, "92.679")
        self.assertEqual(customer_total.total_fatur, "32.196")
        self.assertEqual(customer_total.total_sdo, "31.903")
        self.assertEqual(customer_total.total_valor, "505.528,840")

        report_total = ReportTotal.objects.get(parsed_report=parsed)
        self.assertEqual(report_total.total_ped, "292.850")
        self.assertEqual(report_total.total_in_prod, "157.851")
        self.assertEqual(report_total.total_fatur, "36.279")
        self.assertEqual(report_total.total_sdo, "72.454")
        self.assertEqual(report_total.total_valor, "2.078.254,440")

    
    @patch('reports.services.report_persistence.assemble_report')
    def test_persist_report_creates_full_structure(self, mock_assemble):
        """Test successful persistence of a full parsed report structure."""
        # Mock parser output matching service expectations
        sample_output = {
            'metadata': {
                'generated_date': '2023-10-01',
                'generated_time': '12:00:00'
            },
            'customers': [
                {
                    'representative': 'Rep1',
                    'customer_name': 'Customer A',
                    'items': [
                        {
                            'est': 'EST1',
                            'pedido': 'PED1',
                            'seq': '1',
                            'descricao': 'Desc1',
                            'espess': '10',
                            'larg': '20',
                            'compr': '30',
                            'ord_prod': 'ORD001',
                            'sit_ordem': 'Active',
                            'dt_entr': '2023-01-01',
                            'aa': '2023',
                            'qt_ped': '10',
                            'qt_pc': '5',
                            'qt_prod': '10',
                            'qt_fatur': '5',
                            'sdo_estoq': '0',
                            'sit': 'OK',
                            'pre_liq': '100.0',
                            'pf': '110.0',
                            'vlr_peca': '10.0',
                            'pag': 'Paid',
                            'transp': 'Trans',
                            'cr_pro': 'CR1',
                            'cr_fat': 'CR2',
                            'o_compra': 'OC1',
                            'item_cli': 'IC1',
                            'mnf': 'MNF1',
                            'continuations': [
                                {
                                    'ord_prod': 'ORD001',
                                    'sit_ordem': 'Continued',
                                    'qt_prod': '5',
                                    'sit': 'Pending'
                                }
                            ]
                        }
                    ],
                    'totals': {
                        'client_totals': [
                            {
                                'total_ped': '10',
                                'total_in_prod': '5',
                                'total_fatur': '5',
                                'total_sdo': '0',
                                'total_valor': '100.0'
                            }
                        ],
                    }
                }
            ],
            'totals': {
                'grand_totals': [
                    {
                        'total_ped': '10',
                        'total_in_prod': '5',
                        'total_fatur': '5',
                        'total_sdo': '0',
                        'total_valor': '100.0'
                    }
                ],
            }
        }
        mock_assemble.return_value = sample_output

        # Persist the report
        persist_report(self.uploaded_report)

        # Validate ParsedReport
        parsed_report = ParsedReport.objects.get(uploaded_report=self.uploaded_report)
        self.assertEqual(parsed_report.generated_date, '2023-10-01')
        self.assertEqual(parsed_report.generated_time, '12:00:00')

        # Validate CustomerSection
        customer_section = CustomerSection.objects.get(parsed_report=parsed_report)
        self.assertEqual(customer_section.representative, 'Rep1')
        self.assertEqual(customer_section.customer_name, 'Customer A')

        # Validate ParsedItem
        parsed_item = ParsedItem.objects.get(customer_section=customer_section)
        self.assertEqual(parsed_item.ord_prod, 'ORD001')
        self.assertEqual(parsed_item.qt_prod, '10')

        # Validate ContinuationRow
        continuation = ContinuationRow.objects.get(parsed_item=parsed_item)
        self.assertEqual(continuation.qt_prod, '5')

        # Validate CustomerTotal
        customer_total = CustomerTotal.objects.get(customer_section=customer_section)
        self.assertEqual(customer_total.total_ped, '10')
        self.assertEqual(customer_total.total_valor, '100.0')

        # Validate ReportTotal
        report_total = ReportTotal.objects.get(parsed_report=parsed_report)
        self.assertEqual(report_total.total_ped, '10')
        self.assertEqual(report_total.total_valor, '100.0')

    @patch('reports.services.report_persistence.assemble_report')
    def test_persist_invalid_data_failure(self, mock_assemble):
        """Test failure when persisting invalid or incomplete data."""
        invalid_output = {
            'metadata': {'generated_date': None, 'generated_time': None},
            'customers': [],  # No customers
            'totals': {}
        }
        mock_assemble.return_value = invalid_output

        with self.assertRaisesMessage(
            ReportProcessingError,
            "Parsed report metadata is missing generated_date.",
        ):
            persist_report(self.uploaded_report)

        self.assertEqual(ParsedReport.objects.count(), 0)
        self.assertEqual(CustomerSection.objects.count(), 0)
        self.assertEqual(ParsedItem.objects.count(), 0)
        self.assertEqual(ContinuationRow.objects.count(), 0)
        self.assertEqual(CustomerTotal.objects.count(), 0)
        self.assertEqual(ReportTotal.objects.count(), 0)

    @patch('reports.services.report_persistence.assemble_report')
    def test_persist_report_requires_grand_totals(self, mock_assemble):
        invalid_output = {
            'metadata': {
                'generated_date': '2023-10-01',
                'generated_time': '12:00:00',
            },
            'customers': [
                {
                    'representative': 'Rep1',
                    'customer_name': 'Customer A',
                    'items': [],
                    'totals': {'client_totals': []},
                }
            ],
            'totals': {'grand_totals': []},
        }
        mock_assemble.return_value = invalid_output

        with self.assertRaisesMessage(
            ReportProcessingError,
            "Parsed report must include at least one grand total record.",
        ):
            persist_report(self.uploaded_report)

        self.assertEqual(ParsedReport.objects.count(), 0)
        self.assertEqual(CustomerSection.objects.count(), 0)
        self.assertEqual(ParsedItem.objects.count(), 0)
        self.assertEqual(ContinuationRow.objects.count(), 0)
        self.assertEqual(CustomerTotal.objects.count(), 0)
        self.assertEqual(ReportTotal.objects.count(), 0)

    @patch('reports.services.report_persistence.ContinuationRow.objects.create')
    @patch('reports.services.report_persistence.assemble_report')
    def test_persist_report_rolls_back_all_records_when_nested_create_fails(
        self,
        mock_assemble,
        mock_create_continuation,
    ):
        sample_output = {
            'metadata': {
                'generated_date': '2023-10-01',
                'generated_time': '12:00:00'
            },
            'customers': [
                {
                    'representative': 'Rep1',
                    'customer_name': 'Customer A',
                    'items': [
                        {
                            'est': 'EST1',
                            'pedido': 'PED1',
                            'seq': '1',
                            'descricao': 'Desc1',
                            'espess': '10',
                            'larg': '20',
                            'compr': '30',
                            'ord_prod': 'ORD001',
                            'sit_ordem': 'Active',
                            'dt_entr': '2023-01-01',
                            'aa': '2023',
                            'qt_ped': '10',
                            'qt_pc': '5',
                            'qt_prod': '10',
                            'qt_fatur': '5',
                            'sdo_estoq': '0',
                            'sit': 'OK',
                            'pre_liq': '100.0',
                            'pf': '110.0',
                            'vlr_peca': '10.0',
                            'pag': 'Paid',
                            'transp': 'Trans',
                            'cr_pro': 'CR1',
                            'cr_fat': 'CR2',
                            'o_compra': 'OC1',
                            'item_cli': 'IC1',
                            'mnf': 'MNF1',
                            'continuations': [
                                {
                                    'ord_prod': 'ORD001',
                                    'sit_ordem': 'Continued',
                                    'qt_prod': '5',
                                    'sit': 'Pending'
                                }
                            ]
                        }
                    ],
                    'totals': {
                        'client_totals': [
                            {
                                'total_ped': '10',
                                'total_in_prod': '5',
                                'total_fatur': '5',
                                'total_sdo': '0',
                                'total_valor': '100.0'
                            }
                        ],
                    }
                }
            ],
            'totals': {
                'grand_totals': [
                    {
                        'total_ped': '10',
                        'total_in_prod': '5',
                        'total_fatur': '5',
                        'total_sdo': '0',
                        'total_valor': '100.0'
                    }
                ],
            }
        }
        mock_assemble.return_value = sample_output
        mock_create_continuation.side_effect = IntegrityError("nested write failed")

        with self.assertRaises(IntegrityError):
            persist_report(self.uploaded_report)

        self.assertEqual(ParsedReport.objects.count(), 0)
        self.assertEqual(CustomerSection.objects.count(), 0)
        self.assertEqual(ParsedItem.objects.count(), 0)
        self.assertEqual(ContinuationRow.objects.count(), 0)
        self.assertEqual(CustomerTotal.objects.count(), 0)
        self.assertEqual(ReportTotal.objects.count(), 0)
