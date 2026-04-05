from django.db import models


class UploadedReport(models.Model):
    file = models.FileField(upload_to="reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        filename = self.file.name.rsplit("/", maxsplit=1)[-1] if self.file else "no-file"
        return f"UploadedReport #{self.pk or 'new'} - {filename}"