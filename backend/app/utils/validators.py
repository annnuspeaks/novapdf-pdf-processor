from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import settings


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}


async def validate_upload_size(file: UploadFile) -> None:
    """Reject uploads exceeding the configured size limit."""

    max_size = settings.max_upload_size_mb * 1024 * 1024
    total_size = 0

    while True:
        chunk = await file.read(1024 * 1024)

        if not chunk:
            break

        total_size += len(chunk)

        if total_size > max_size:
            await file.seek(0)
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds the {settings.max_upload_size_mb} MB limit.",
            )

    await file.seek(0)


def validate_extension(
    filename: str | None,
    allowed_extensions: set[str],
) -> None:
    """Validate a file's extension."""

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    extension = Path(filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=415,
            detail="This file extension is not supported.",
        )