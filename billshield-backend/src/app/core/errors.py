from __future__ import annotations

from typing import Any


class AppError(Exception):
    """Base exception for the application."""

    def __init__(self, code: str, message: str, status_code: int = 400, details: dict[str, Any] | None = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class HouseholdNotFoundError(AppError):
    def __init__(self, household_id: str):
        super().__init__(
            code="HOUSEHOLD_NOT_FOUND",
            message="We could not find that household profile.",
            status_code=404,
            details={"householdId": household_id},
        )


class BillNotFoundError(AppError):
    def __init__(self, bill_id: str):
        super().__init__(
            code="BILL_NOT_FOUND",
            message="We could not find that bill.",
            status_code=404,
            details={"billId": bill_id},
        )


class UnsupportedFileTypeError(AppError):
    def __init__(self, file_type: str):
        super().__init__(
            code="UNSUPPORTED_FILE_TYPE",
            message=f"File type '{file_type}' is not supported. Please upload a PDF, PNG, JPG, or JPEG file.",
            status_code=415,
            details={"fileType": file_type},
        )


class UploadTooLargeError(AppError):
    def __init__(self, file_size_bytes: int, max_size_bytes: int):
        super().__init__(
            code="UPLOAD_TOO_LARGE",
            message=f"File size ({file_size_bytes / 1024 / 1024:.1f}MB) exceeds the maximum allowed size ({max_size_bytes / 1024 / 1024:.0f}MB).",
            status_code=413,
            details={"fileSizeBytes": file_size_bytes, "maxSizeBytes": max_size_bytes},
        )


class BillAlreadyDeletedError(AppError):
    def __init__(self, bill_id: str):
        super().__init__(
            code="BILL_ALREADY_DELETED",
            message="That bill has already been deleted.",
            status_code=400,
            details={"billId": bill_id},
        )


class InvalidScenarioError(AppError):
    def __init__(self, message: str = "The scenario could not be simulated with the provided data."):
        super().__init__(
            code="INVALID_SCENARIO",
            message=message,
            status_code=400,
        )


class RecommendationNotFoundError(AppError):
    def __init__(self, household_id: str):
        super().__init__(
            code="RECOMMENDATIONS_NOT_FOUND",
            message="No recommendations could be generated for this household.",
            status_code=404,
            details={"householdId": household_id},
        )
