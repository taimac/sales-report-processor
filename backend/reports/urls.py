from django.urls import path

from .views import ReportUploadView

# App-level URL patterns for the reports module.
# Final endpoint becomes:
# /api/reports/upload/
urlpatterns = [
    path("upload/", ReportUploadView.as_view(), name="report-upload"),
]