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