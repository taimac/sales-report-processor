from django.test import TestCase

from reports.models import (
    CustomerSection,
    CustomerTotal,
    ParsedItem,
    ParsedReport,
    ReportTotal,
    UploadedReport,
)


class DashboardViewTests(TestCase):
    dashboard_url = "/dashboard/"

    def _create_dashboard_report(self, file_name, generated_date, generated_time):
        uploaded_report = UploadedReport.objects.create(file=f"reports/{file_name}")
        parsed_report = ParsedReport.objects.create(
            uploaded_report=uploaded_report,
            generated_date=generated_date,
            generated_time=generated_time,
        )
        ReportTotal.objects.create(
            parsed_report=parsed_report,
            total_ped="12.000",
            total_in_prod="5.000",
            total_fatur="3.000",
            total_sdo="4.000",
            total_valor="150.000,000",
        )
        return parsed_report

    def test_dashboard_returns_200_with_empty_state_when_no_reports_exist(self):
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum relatorio processado disponivel ainda")

    def test_dashboard_uses_latest_parsed_report(self):
        self._create_dashboard_report("older.txt", "12/04/2026", "08:00:00")
        latest = self._create_dashboard_report("latest.txt", "13/04/2026", "09:00:00")

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "reports/latest.txt")
        self.assertEqual(response.context["dashboard"]["report_meta"]["report_id"], latest.id)

    def test_dashboard_renders_summary_action_queue_and_tables(self):
        parsed_report = self._create_dashboard_report("actionable.txt", "13/04/2026", "09:00:00")

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
        ParsedItem.objects.create(
            customer_section=customer,
            pedido="402973",
            descricao="TIRA ZC",
            ord_prod="9.148.823",
            sit_ordem="LC10",
            dt_entr="12/04/2026",
            qt_ped="2.000",
            qt_prod="857",
            qt_fatur="0",
            sdo_estoq="1.582",
            sit="Em Produ",
            transp="RODOTREM",
        )

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Indicadores Principais")
        self.assertContains(response, "Visao Operacional")
        self.assertContains(response, "Pedidos em Atraso vs Total de Itens/Pedidos")
        self.assertContains(response, "Peso em Atraso por Cliente")
        self.assertContains(response, "Produzido com Data Vencida por Cliente")
        self.assertContains(response, "Valor em Risco por Cliente")
        self.assertContains(response, "Fila de Prioridades")
        self.assertContains(response, "Flag Principal")
        self.assertContains(response, "Acao Sugerida")
        self.assertContains(response, "Carteira em Foco")
        self.assertContains(response, "Prioridade da Conta")
        self.assertContains(response, "Motivo de Foco")
        self.assertContains(response, "Excecoes Operacionais")
        self.assertContains(response, "Clientes em Evidencia")
        self.assertNotContains(response, "Status dos Pedidos")
        self.assertNotContains(response, "Producao a Acompanhar")
        self.assertContains(response, "Entrega em Atencao")
        self.assertContains(response, "Cliente de Alto Valor + Flags")
        self.assertContains(response, "Cliente 360")
        self.assertContains(response, "Conta selecionada a partir da Carteira em Foco")
        self.assertContains(response, "Handoff da Carteira")
        self.assertContains(response, "Motivo da selecao")
        self.assertContains(response, "Timeline de Entregas")
        self.assertContains(response, "O.Compra")
        self.assertContains(response, "Item Cli")
        self.assertContains(response, "Larg")
        self.assertContains(response, "Qt Ped")
        self.assertContains(response, "Sdo Estoq")
        self.assertNotContains(response, "Rankings")
        self.assertNotContains(response, "Matriz de Flags")
        self.assertNotContains(response, "Fila de Acao")
        self.assertContains(response, "Pedidos em Atraso")
        self.assertContains(response, "Falta Produzir")
        self.assertContains(response, "Peso em Atraso")
        self.assertContains(response, "Entrega Esse Mes")
        self.assertContains(response, "Produzido Com Data Vencida")
        self.assertContains(response, "Valor em Pedidos")
        self.assertContains(response, "Quantidade Pedida")
        self.assertContains(response, "Preco Medio")
        self.assertNotContains(response, '<span class="label">Em Producao</span>')
        self.assertContains(response, "UTIMIL")
        self.assertContains(response, "402973")
        self.assertContains(response, "31.649,460")

        rendered_html = response.content.decode("utf-8")
        self.assertLess(
            rendered_html.index("Excecoes Operacionais"),
            rendered_html.index("Fila de Prioridades"),
        )
        self.assertLess(
            rendered_html.index("Fila de Prioridades"),
            rendered_html.index("Carteira em Foco"),
        )
        self.assertLess(
            rendered_html.index("Carteira em Foco"),
            rendered_html.index("Clientes em Evidencia"),
        )
        self.assertLess(
            rendered_html.index("Clientes em Evidencia"),
            rendered_html.index("Cliente 360"),
        )
