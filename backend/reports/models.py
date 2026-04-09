from django.db import models


class UploadedReport(models.Model):
    file = models.FileField(upload_to="reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        filename = self.file.name.rsplit("/", maxsplit=1)[-1] if self.file else "no-file"
        return f"UploadedReport #{self.pk or 'new'} - {filename}"
    

class ParsedReport(models.Model):
    """
    Represents a parsed TXT report.

    Top-level entity linking the uploaded file
    to structured parsed data.
    """

    uploaded_report = models.ForeignKey(
        "reports.UploadedReport",
        on_delete=models.CASCADE,
        related_name="parsed_reports",
    )

    generated_date = models.CharField(max_length=20)
    generated_time = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ParsedReport {self.id} - {self.generated_date} {self.generated_time}"
    
class CustomerSection(models.Model):
    """
    Represents a customer block inside a parsed report.
    """

    parsed_report = models.ForeignKey(
        "reports.ParsedReport",
        on_delete=models.CASCADE,
        related_name="customers",
    )

    representative = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer_name} ({self.representative})"
    
class ParsedItem(models.Model):
    """
    Represents a main row (item) in the parsed report.
    """

    customer_section = models.ForeignKey(
        "reports.CustomerSection",
        on_delete=models.CASCADE,
        related_name="items",
    )

    # --- Identity / Product ---
    est = models.CharField(max_length=10, blank=True)
    pedido = models.CharField(max_length=20, blank=True)
    seq = models.CharField(max_length=10, blank=True)

    descricao = models.CharField(max_length=255, blank=True)
    espess = models.CharField(max_length=20, blank=True)
    larg = models.CharField(max_length=20, blank=True)
    compr = models.CharField(max_length=20, blank=True)

    # --- Operational ---
    ord_prod = models.CharField(max_length=20, blank=True)
    sit_ordem = models.CharField(max_length=50, blank=True)
    dt_entr = models.CharField(max_length=20, blank=True)
    aa = models.CharField(max_length=10, blank=True)

    # --- Quantities ---
    qt_ped = models.CharField(max_length=20, blank=True)
    qt_pc = models.CharField(max_length=20, blank=True)
    qt_prod = models.CharField(max_length=20, blank=True)
    qt_fatur = models.CharField(max_length=20, blank=True)
    sdo_estoq = models.CharField(max_length=20, blank=True)

    sit = models.CharField(max_length=20, blank=True)

    # --- Commercial ---
    pre_liq = models.CharField(max_length=20, blank=True)
    pf = models.CharField(max_length=20, blank=True)
    vlr_peca = models.CharField(max_length=20, blank=True)

    pag = models.CharField(max_length=20, blank=True)
    transp = models.CharField(max_length=100, blank=True)

    # --- Credit / Reference ---
    cr_pro = models.CharField(max_length=20, blank=True)
    cr_fat = models.CharField(max_length=20, blank=True)
    o_compra = models.CharField(max_length=50, blank=True)
    item_cli = models.CharField(max_length=50, blank=True)
    mnf = models.CharField(max_length=50, blank=True)

    # --- Traceability ---
    raw_line = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pedido} - {self.descricao}"
    
class ContinuationRow(models.Model):
    """
    Represents a continuation row linked to a ParsedItem.
    """

    parsed_item = models.ForeignKey(
        "reports.ParsedItem",
        on_delete=models.CASCADE,
        related_name="continuations",
    )

    ord_prod = models.CharField(max_length=20, blank=True)
    sit_ordem = models.CharField(max_length=50, blank=True)
    qt_prod = models.CharField(max_length=20, blank=True)
    sit = models.CharField(max_length=20, blank=True)

    raw_line = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ord_prod} - {self.sit_ordem}"