from pathlib import Path

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UploadedReport


class ReportUploadView(APIView):
    """
    Handle supplier report uploads for the SRP MVP.

    Current scope:
        - accept multipart file upload
        - validate file presence
        - validate supported file extensions (.txt, .pdf)
        - persist the file using UploadedReport
        - return clear success and error responses

    Expected request:
        POST /api/reports/upload/
        Content-Type: multipart/form-data
        Form field: "file"

    Success response:
        201 Created
        {
            "id": <int>,
            "file": "<relative stored path>",
            "uploaded_at": "<iso datetime>",
            "message": "File uploaded successfully."
        }

    Error response:
        400 Bad Request
        {
            "error": "No file provided."
        }
    """

    # These parsers allow DRF to correctly read multipart file uploads
    # and regular form fields from the request body.
    parser_classes = [MultiPartParser, FormParser]
    allowed_extensions = {".txt", ".pdf"}

    def post(self, request, *args, **kwargs):
        """
        Receive an uploaded file and create an UploadedReport record.

        Flow:
            1. Read the "file" field from request.FILES
            2. Reject the request if no file is present
            3. Save the file through the UploadedReport model
            4. Return a 201 response with the stored file metadata
        """
        uploaded_file = request.FILES.get("file")

        # Minimal validation for SRP-5:
        # only ensure that a file was actually sent in the request.
        if uploaded_file is None:
            return Response(
                {"error": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_extension = Path(uploaded_file.name).suffix.lower()

        if file_extension not in self.allowed_extensions:
            return Response(
                {"error": "Unsupported file type. Only .txt and .pdf files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Creating the model instance causes Django to:
        # - save the file under MEDIA_ROOT / "reports/"
        # - store the relative file path in the database
        # - automatically set uploaded_at because of auto_now_add=True
        report = UploadedReport.objects.create(file=uploaded_file)

        return Response(
            {
                "id": report.id,
                "file": report.file.name,
                "uploaded_at": report.uploaded_at,
                "message": "File uploaded successfully.",
            },
            status=status.HTTP_201_CREATED,
        )