from rest_framework import serializers

from .models import (
    ContinuationRow,
    CustomerSection,
    CustomerTotal,
    ParsedItem,
    ParsedReport,
    ReportTotal,
)


class ContinuationRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContinuationRow
        fields = [
            "id",
            "ord_prod",
            "sit_ordem",
            "qt_prod",
            "sit",
            "raw_line",
            "created_at",
        ]
        read_only_fields = fields


class ParsedItemSerializer(serializers.ModelSerializer):
    continuations = ContinuationRowSerializer(many=True, read_only=True)

    class Meta:
        model = ParsedItem
        fields = [
            "id",
            "est",
            "pedido",
            "seq",
            "descricao",
            "espess",
            "larg",
            "compr",
            "ord_prod",
            "sit_ordem",
            "dt_entr",
            "aa",
            "qt_ped",
            "qt_pc",
            "qt_prod",
            "qt_fatur",
            "sdo_estoq",
            "sit",
            "pre_liq",
            "pf",
            "vlr_peca",
            "pag",
            "transp",
            "cr_pro",
            "cr_fat",
            "o_compra",
            "item_cli",
            "mnf",
            "raw_line",
            "created_at",
            "continuations",
        ]
        read_only_fields = fields


class CustomerTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerTotal
        fields = [
            "id",
            "total_ped",
            "total_in_prod",
            "total_fatur",
            "total_sdo",
            "total_valor",
            "created_at",
        ]
        read_only_fields = fields


class ReportTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTotal
        fields = [
            "id",
            "total_ped",
            "total_in_prod",
            "total_fatur",
            "total_sdo",
            "total_valor",
            "created_at",
        ]
        read_only_fields = fields


class CustomerSectionSerializer(serializers.ModelSerializer):
    total = CustomerTotalSerializer(read_only=True)
    items = ParsedItemSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerSection
        fields = [
            "id",
            "representative",
            "customer_name",
            "created_at",
            "total",
            "items",
        ]
        read_only_fields = fields


class ParsedReportListSerializer(serializers.ModelSerializer):
    uploaded_report_id = serializers.IntegerField(read_only=True)
    uploaded_file = serializers.CharField(source="uploaded_report.file.name", read_only=True)
    report_total = ReportTotalSerializer(source="total", read_only=True)

    class Meta:
        model = ParsedReport
        fields = [
            "id",
            "uploaded_report_id",
            "uploaded_file",
            "generated_date",
            "generated_time",
            "created_at",
            "report_total",
        ]
        read_only_fields = fields


class ParsedReportDetailSerializer(serializers.ModelSerializer):
    uploaded_report_id = serializers.IntegerField(read_only=True)
    uploaded_file = serializers.CharField(source="uploaded_report.file.name", read_only=True)
    report_total = ReportTotalSerializer(source="total", read_only=True)
    customers = CustomerSectionSerializer(many=True, read_only=True)

    class Meta:
        model = ParsedReport
        fields = [
            "id",
            "uploaded_report_id",
            "uploaded_file",
            "generated_date",
            "generated_time",
            "created_at",
            "report_total",
            "customers",
        ]
        read_only_fields = fields
