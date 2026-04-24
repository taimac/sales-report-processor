from datetime import date
from decimal import Decimal

from django.test import TestCase

from reports.models import (
    CustomerSection,
    CustomerTotal,
    ParsedItem,
    ParsedReport,
    ReportTotal,
    UploadedReport,
)
from reports.services.dashboard_service import build_dashboard, parse_decimal


class DashboardServiceTests(TestCase):
    def test_parse_decimal_treats_dot_only_values_as_thousands(self):
        self.assertEqual(parse_decimal("2.000"), 2000)
        self.assertEqual(parse_decimal("12.604"), 12604)
        self.assertEqual(parse_decimal("1.942,550"), Decimal("1942.550"))
        self.assertEqual(parse_decimal("12"), 12000)
        self.assertEqual(parse_decimal("8.5"), 8500)

    def test_build_dashboard_aggregates_summary_and_prioritizes_clients(self):
        uploaded_report = UploadedReport.objects.create(file="reports/dashboard.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="292.850",
            total_in_prod="157.851",
            total_fatur="36.279",
            total_sdo="72.454",
            total_valor="2.078.254,440",
        )

        priority_customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="UTIMIL",
        )
        CustomerTotal.objects.create(
            customer_section=priority_customer,
            total_ped="4.000",
            total_in_prod="3.611",
            total_fatur="0",
            total_sdo="1.582",
            total_valor="31.649,460",
        )
        ParsedItem.objects.create(
            customer_section=priority_customer,
            pedido="402973",
            seq="10",
            descricao="TIRA ZC",
            larg="1.250,00",
            ord_prod="9.148.823",
            sit_ordem="LC10",
            dt_entr="12/04/2026",
            qt_ped="2.000",
            qt_prod="857",
            qt_fatur="0",
            sdo_estoq="1.582",
            sit="Em Produ",
            pre_liq="6,850",
            transp="RODOTREM",
            o_compra="OC-7781",
            item_cli="CLI-10",
        )

        secondary_customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="FLANTECH",
        )
        CustomerTotal.objects.create(
            customer_section=secondary_customer,
            total_ped="1.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="1.000",
            total_valor="8.000,000",
        )
        ParsedItem.objects.create(
            customer_section=secondary_customer,
            pedido="555001",
            seq="10",
            descricao="CHAPA X",
            ord_prod="",
            sit_ordem="",
            dt_entr="",
            qt_ped="1.000",
            qt_prod="0",
            qt_fatur="0",
            sdo_estoq="1.000",
            sit="Pendente",
            pre_liq="8,000",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["summary"]["total_clients"], 2)
        self.assertEqual(dashboard["summary"]["total_ordered"], "292.850")
        self.assertEqual(dashboard["summary"]["pedidos_em_atraso"], 1)
        self.assertEqual(dashboard["summary"]["falta_produzir"], "418")
        self.assertEqual(dashboard["summary"]["em_atraso"], "418")
        self.assertEqual(dashboard["summary"]["produzido_data_vencida"], "1.582")
        self.assertEqual(dashboard["summary"]["entrega_esse_mes"], "2.000")
        self.assertEqual(dashboard["summary"]["average_price"], "7,10")
        self.assertEqual(dashboard["operational_comparison"]["late_lines"], 1)
        self.assertEqual(dashboard["operational_comparison"]["total_lines"], 2)
        self.assertEqual(dashboard["operational_comparison"]["late_pct"], 50)
        self.assertEqual(dashboard["overdue_weight_chart"][0]["customer_name"], "UTIMIL")
        self.assertEqual(dashboard["overdue_weight_chart"][0]["value"], "418")
        self.assertEqual(dashboard["overdue_stock_chart"][0]["customer_name"], "UTIMIL")
        self.assertEqual(dashboard["overdue_stock_chart"][0]["value"], "1.582")
        self.assertEqual(dashboard["overdue_value_chart"][0]["customer_name"], "UTIMIL")
        self.assertEqual(dashboard["overdue_value_chart"][0]["stock_value"], "10.836,70")
        self.assertEqual(dashboard["overdue_value_chart"][0]["delay_value"], "2.863,30")
        self.assertTrue(dashboard["delivery_attention_card"])
        self.assertTrue(dashboard["high_value_card"])
        self.assertTrue(dashboard["clients_with_flags"])
        self.assertEqual(dashboard["client_rows"][0]["customer_name"], "UTIMIL")
        self.assertEqual(dashboard["client_rows"][1]["customer_name"], "FLANTECH")
        self.assertEqual(dashboard["client_rows"][0]["action_flag_count"], 1)
        self.assertEqual(dashboard["client_rows"][0]["dominant_signal_label"], "Entrega em Atencao")
        self.assertIn("entregas vencidas", dashboard["client_rows"][0]["focus_reason"])
        self.assertEqual(
            dashboard["client_rows"][0]["next_reading"],
            "Revisar itens vencidos e cobrar entrega.",
        )
        self.assertEqual(dashboard["worklist_rows"][0]["primary_bucket"], "delivery_attention")
        self.assertEqual(dashboard["worklist_rows"][0]["sit_ordem"], "LC10")

        bucket_counts = dashboard["action_counts"]
        self.assertEqual(bucket_counts["delivery_attention"], 1)
        self.assertEqual(bucket_counts["missing_production_reference"], 1)
        self.assertEqual(bucket_counts["stock_balance"], 2)
        self.assertEqual(bucket_counts["high_value_customer"], 2)
        self.assertEqual(dashboard["exception_panel"][0]["label"], "Entrega em Atencao")
        self.assertEqual(dashboard["client_360"]["customer_name"], "UTIMIL")
        self.assertEqual(
            dashboard["client_360"]["customer_name"],
            dashboard["client_rows"][0]["customer_name"],
        )
        self.assertEqual(dashboard["client_360"]["selected_from"], "Carteira em Foco")
        self.assertEqual(dashboard["client_360"]["selection_rank"], 1)
        self.assertEqual(
            dashboard["client_360"]["selection_reason"],
            dashboard["client_rows"][0]["focus_reason"],
        )
        self.assertEqual(
            dashboard["client_360"]["selection_hint"],
            dashboard["client_rows"][0]["next_reading"],
        )
        self.assertEqual(
            dashboard["client_360"]["dominant_signal_label"],
            dashboard["client_rows"][0]["dominant_signal_label"],
        )
        self.assertEqual(dashboard["client_360"]["critical_item_count"], 1)
        self.assertTrue(dashboard["delivery_timeline"])
        self.assertEqual(dashboard["delivery_timeline"][0]["total_weight"], "2.000")
        timeline_item = dashboard["delivery_timeline"][0]["days"][0]["items"][0]
        self.assertEqual(timeline_item["larg"], "1.250,00")
        self.assertEqual(timeline_item["o_compra"], "OC-7781")
        self.assertEqual(timeline_item["item_cli"], "CLI-10")
        self.assertTrue(dashboard["support_exception_rows"])
        self.assertEqual(
            dashboard["support_exception_rows"][0]["signal_label"],
            "Entrega em Atencao",
        )
        self.assertTrue(dashboard["support_client_rows"])
        self.assertEqual(
            dashboard["support_client_rows"][0]["support_label"],
            "Cliente de Alto Valor + Flags",
        )
        self.assertEqual(
            [section["label"] for section in dashboard["exception_panel"]],
            ["Entrega em Atencao", "Sem Ordem de Producao"],
        )
        missing_orders = dashboard["exception_panel"][1]["items"]
        self.assertEqual(len(missing_orders), 1)
        self.assertEqual(missing_orders[0]["customer_name"], "FLANTECH")

    def test_build_dashboard_counts_late_lines_by_unique_pedido_and_seq(self):
        uploaded_report = UploadedReport.objects.create(file="reports/late-lines.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="4.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="0",
            total_valor="10.000,000",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="LATE",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="4.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="0",
            total_valor="10.000,000",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="100001",
            seq="10",
            descricao="ITEM 1",
            dt_entr="12/04/2026",
            qt_ped="1.000",
            qt_prod="0",
            qt_fatur="0",
            sdo_estoq="0",
            sit="Pendente",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="100001",
            seq="20",
            descricao="ITEM 2",
            dt_entr="12/04/2026",
            qt_ped="1.000",
            qt_prod="0",
            qt_fatur="0",
            sdo_estoq="0",
            sit="Pendente",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["summary"]["pedidos_em_atraso"], 2)
        self.assertEqual(dashboard["operational_comparison"]["total_lines"], 2)
        self.assertEqual(dashboard["operational_comparison"]["late_pct"], 100)

    def test_build_dashboard_prefers_item_level_average_price_when_items_match_report_total(self):
        uploaded_report = UploadedReport.objects.create(file="reports/avg-price.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="2.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="2.000",
            total_valor="4.000,000",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="MEDIA",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="2.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="2.000",
            total_valor="4.000,000",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="700001",
            seq="10",
            descricao="ITEM MEDIA",
            dt_entr="13/04/2026",
            qt_ped="2.000",
            qt_prod="0",
            qt_fatur="0",
            sdo_estoq="2.000",
            sit="Pendente",
            pre_liq="6,000",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["summary"]["average_price"], "6,00")

    def test_operational_charts_clamp_negative_overdue_remaining_to_zero(self):
        uploaded_report = UploadedReport.objects.create(file="reports/operational-risk.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="12.000",
            total_in_prod="12.031",
            total_fatur="12.031",
            total_sdo="0",
            total_valor="90.000,000",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="FLANTECH",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="12.000",
            total_in_prod="12.031",
            total_fatur="12.031",
            total_sdo="0",
            total_valor="90.000,000",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="401770",
            seq="10",
            descricao="ITEM NEGATIVO",
            dt_entr="12/04/2026",
            qt_ped="12.000",
            qt_prod="12.031",
            qt_fatur="12.031",
            sdo_estoq="0",
            pre_liq="9,290",
            sit="Fat Parc",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["summary"]["pedidos_em_atraso"], 0)
        self.assertEqual(dashboard["summary"]["em_atraso"], "0")
        self.assertEqual(dashboard["operational_comparison"]["late_lines"], 0)
        self.assertEqual(dashboard["operational_comparison"]["late_pct"], 0)
        self.assertEqual(dashboard["overdue_weight_chart"], [])
        self.assertEqual(dashboard["overdue_stock_chart"], [])
        self.assertEqual(dashboard["overdue_value_chart"], [])

    def test_operational_charts_add_outros_bucket_when_more_than_top_five_clients_exist(self):
        uploaded_report = UploadedReport.objects.create(file="reports/outros-bucket.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="21.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="21.000",
            total_valor="126.000,000",
        )

        for index in range(1, 7):
            customer = CustomerSection.objects.create(
                parsed_report=parsed_report,
                representative="MACIEL",
                customer_name=f"CLIENTE {index}",
            )
            CustomerTotal.objects.create(
                customer_section=customer,
                total_ped="1.000",
                total_in_prod="0",
                total_fatur="0",
                total_sdo=f"{index}.000",
                total_valor=f"{index * 10}.000,000",
            )
            ParsedItem.objects.create(
                customer_section=customer,
                pedido=f"2000{index}",
                seq="10",
                descricao=f"ITEM {index}",
                dt_entr="12/04/2026",
                qt_ped=f"{index}.000",
                qt_prod="0",
                qt_fatur="0",
                sdo_estoq=f"{index}.000",
                pre_liq="6,000",
                sit="Pendente",
            )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(len(dashboard["overdue_stock_chart"]), 6)
        self.assertEqual(dashboard["overdue_stock_chart"][-1]["customer_name"], "Outros")
        self.assertEqual(dashboard["overdue_stock_chart"][-1]["value"], "1.000")
        self.assertEqual(dashboard["overdue_value_chart"][-1]["customer_name"], "Outros")

    def test_build_dashboard_marks_high_value_customer_for_top_open_value(self):
        uploaded_report = UploadedReport.objects.create(file="reports/high-value.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="10.000",
            total_in_prod="4.000",
            total_fatur="2.000",
            total_sdo="4.000",
            total_valor="120.000,000",
        )

        for index, (name, total_valor) in enumerate(
            [
                ("ALPHA", "40.000,000"),
                ("BETA", "30.000,000"),
                ("GAMMA", "20.000,000"),
                ("DELTA", "10.000,000"),
            ],
            start=1,
        ):
            customer = CustomerSection.objects.create(
                parsed_report=parsed_report,
                representative="MACIEL",
                customer_name=name,
            )
            CustomerTotal.objects.create(
                customer_section=customer,
                total_ped="1.000",
                total_in_prod="0",
                total_fatur="0",
                total_sdo="1.000",
                total_valor=total_valor,
            )
            ParsedItem.objects.create(
                customer_section=customer,
                pedido=f"50000{index}",
                descricao=f"MATERIAL {index}",
                qt_ped="1.000",
                qt_prod="0",
                qt_fatur="0",
                sdo_estoq="1.000",
                sit="Pendente",
            )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))
        action_rows = {row["customer_name"]: row for row in dashboard["worklist_rows"]}

        self.assertIn("high_value_customer", action_rows["ALPHA"]["signals"])
        self.assertIn("high_value_customer", action_rows["BETA"]["signals"])
        self.assertIn("high_value_customer", action_rows["GAMMA"]["signals"])
        self.assertNotIn("high_value_customer", action_rows["DELTA"]["signals"])
        self.assertIn("Cliente de Alto Valor", dashboard["client_360"]["flags"])

    def test_build_dashboard_flags_credit_block_and_uses_continuation_order_status(self):
        uploaded_report = UploadedReport.objects.create(file="reports/credit-block.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="5.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="0",
            total_valor="50.000,000",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="BLOQUEADO",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="5.000",
            total_in_prod="0",
            total_fatur="0",
            total_sdo="0",
            total_valor="50.000,000",
        )
        item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="700001",
            seq="10",
            descricao="CHAPA FQ",
            ord_prod="",
            sit_ordem="",
            dt_entr="",
            qt_ped="",
            qt_prod="",
            qt_fatur="",
            sdo_estoq="",
            sit="",
            cr_pro="Sim",
            cr_fat="Nao",
        )
        item.continuations.create(
            ord_prod="9.999.001",
            sit_ordem="LC12",
            qt_prod="0",
            sit="Aguardando",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["action_counts"]["credit_block"], 1)
        self.assertEqual(dashboard["worklist_rows"][0]["sit_ordem"], "LC12")
        self.assertEqual(dashboard["worklist_rows"][0]["ord_prod"], "9.999.001")
        self.assertEqual(dashboard["worklist_rows"][0]["cr_pro"], "Sim")

    def test_credit_block_requires_explicit_nao(self):
        uploaded_report = UploadedReport.objects.create(file="reports/no-block.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="LIVRE",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="800001",
            seq="10",
            descricao="ITEM LIVRE",
            ord_prod="9.000.001",
            qt_ped="1.000",
            qt_prod="0",
            qt_fatur="0",
            sdo_estoq="1.000",
            sit="Em Produ",
            cr_pro="Sim",
            cr_fat="Sim",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["action_counts"]["credit_block"], 0)
        self.assertFalse(dashboard["credit_blocked_orders"])

    def test_missing_production_reference_keeps_blank_orders_without_quantities(self):
        uploaded_report = UploadedReport.objects.create(file="reports/no-op.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="GPANIZ",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="404651",
            seq="20",
            descricao="CHAPA FQ 2,65",
            ord_prod="",
            sit_ordem="",
            dt_entr="",
            qt_ped="",
            qt_prod="",
            qt_fatur="",
            sdo_estoq="",
            sit="",
            cr_pro="Sim",
            cr_fat="Sim",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(dashboard["action_counts"]["missing_production_reference"], 1)
        self.assertEqual(
            dashboard["exception_panel"][1]["items"][0]["pedido"],
            "404651",
        )

    def test_credit_blocked_orders_section_lists_only_explicit_blocks(self):
        uploaded_report = UploadedReport.objects.create(file="reports/credit-list.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="METALMATRIX",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="405197",
            seq="10",
            descricao="ITEM BLOQUEADO",
            ord_prod="",
            sit_ordem="",
            dt_entr="15/04/2026",
            qt_ped="",
            qt_prod="",
            qt_fatur="",
            sdo_estoq="",
            sit="",
            cr_pro="Nao",
            cr_fat="Nao",
        )
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="405198",
            seq="10",
            descricao="ITEM LIVRE",
            ord_prod="",
            sit_ordem="",
            dt_entr="15/04/2026",
            qt_ped="",
            qt_prod="",
            qt_fatur="",
            sdo_estoq="",
            sit="",
            cr_pro="Sim",
            cr_fat="Sim",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(len(dashboard["credit_blocked_orders"]), 1)
        self.assertEqual(dashboard["credit_blocked_orders"][0]["pedido"], "405197")

    def test_build_dashboard_combines_main_and_continuation_order_references(self):
        uploaded_report = UploadedReport.objects.create(file="reports/multi-order.txt")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date="13/04/2026",
            generated_time="09:15:00",
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="2.000",
            total_in_prod="1.000",
            total_fatur="0",
            total_sdo="1.000",
            total_valor="10.000,000",
        )

        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative="MACIEL",
            customer_name="UTIMIL",
        )
        CustomerTotal.objects.create(
            customer_section=customer,
            total_ped="2.000",
            total_in_prod="1.000",
            total_fatur="0",
            total_sdo="1.000",
            total_valor="10.000,000",
        )
        item = ParsedItem.objects.create(
            customer_section=customer,
            pedido="402973",
            seq="10",
            descricao="TIRA ZC",
            ord_prod="9.148.823",
            sit_ordem="EMBAL-A24",
            dt_entr="10/04/2026",
            qt_ped="2.000",
            qt_prod="857",
            qt_fatur="0",
            sdo_estoq="1.000",
            sit="Em Produ",
        )
        item.continuations.create(
            ord_prod="9.148.942",
            sit_ordem="EMBAL-A24",
            qt_prod="1.172",
            sit="Em Produ",
        )

        dashboard = build_dashboard(parsed_report, today=date(2026, 4, 13))

        self.assertEqual(
            dashboard["worklist_rows"][0]["ord_prod"],
            "9.148.823 - 9.148.942",
        )
        self.assertEqual(
            dashboard["worklist_rows"][0]["sit_ordem"],
            "EMBAL-A24",
        )
