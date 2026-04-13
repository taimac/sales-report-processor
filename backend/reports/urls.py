from django.urls import path

from .views import ParsedReportDetailView, ParsedReportListView, ReportUploadView

# App-level URL patterns for the reports module.
# Final endpoint becomes:
# /api/reports/upload/
urlpatterns = [
    path("", ParsedReportListView.as_view(), name="parsed-report-list"),
    path("<int:pk>/", ParsedReportDetailView.as_view(), name="parsed-report-detail"),
    path("upload/", ReportUploadView.as_view(), name="report-upload"),
]
