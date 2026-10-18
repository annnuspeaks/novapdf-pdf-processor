from io import BytesIO

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse, PlainTextResponse

from app.config import settings

from app.services.pdf_service import images_to_pdf
from app.services.merge_service import merge_pdfs
from app.services.split_service import extract_pdf_pages
from app.services.rotate_service import rotate_pdf
from app.services.extract_text_service import extract_text_from_pdf

from app.utils.validators import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_PDF_EXTENSIONS,
    validate_extension,
    validate_upload_size,
)

router = APIRouter(prefix="/api")


@router.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@router.post("/tools/images-to-pdf", tags=["PDF Tools"])
async def convert_images_to_pdf(
    files: list[UploadFile]=File(..., description="JPEG or PNG images"),
):
    """Convert uploaded JPEG/PNG images into a downloadable PDF."""

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Upload at least one image.",
        )

    if len(files) > 20:
        raise HTTPException(
            status_code=400,
            detail="Upload a maximum of 20 images per request.",
        )

    image_contents: list[bytes] = []

    try:
        for file in files:
            validate_extension(
                file.filename,
                ALLOWED_IMAGE_EXTENSIONS,
            )

            await validate_upload_size(file)

            content = await file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="Empty files are not supported.",
                )

            image_contents.append(content)

        pdf_bytes = images_to_pdf(image_contents)

        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="nova-images.pdf"',
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
            },
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        for file in files:
            await file.close()


@router.post("/tools/merge-pdfs", tags=["PDF Tools"])
async def merge_pdf_files(
    files: list[UploadFile]=File(
        ...,
        description="Select at least two PDF files.",
    ),
):
    """Merge multiple PDF files into one downloadable PDF."""

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Please select at least two PDF files to merge.",
        )

    if len(files) < 2:
        raise HTTPException(
            status_code=400,
            detail="Please choose more than one PDF file.",
        )

    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="You can merge a maximum of 10 PDF files at a time.",
        )

    pdf_contents: list[bytes] = []

    try:
        for file in files:
            filename = file.filename or ""

            # Reject unsupported file extensions first.
            if not filename.lower().endswith(".pdf"):
                raise HTTPException(
                    status_code=415,
                    detail=(
                        f"'{filename}' is not a PDF file. "
                        "Please choose PDF files only."
                    ),
                )

            await validate_upload_size(file)

            content = await file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"'{filename}' is empty. "
                        "Please choose a valid PDF file."
                    ),
                )

            # Check the basic PDF signature.
            if not content.startswith(b"%PDF-"):
                raise HTTPException(
                    status_code=415,
                    detail=(
                        f"'{filename}' is not a valid PDF file. "
                        "Please choose a PDF document."
                    ),
                )

            pdf_contents.append(content)

        merged_bytes = merge_pdfs(pdf_contents)

        return StreamingResponse(
            BytesIO(merged_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    'attachment; filename="nova-merged.pdf"'
                ),
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
            },
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        for file in files:
            await file.close()


@router.post("/tools/extract-pages", tags=["PDF Tools"])
async def extract_pdf_pages_endpoint(
    file: UploadFile=File(
        ...,
        description="Upload the PDF from which pages should be extracted.",
    ),
    pages: str=Form(
        ...,
        description="Page numbers or ranges, e.g. 1,3,5 or 2-5.",
    ),
):
    """Extract selected pages from a PDF."""

    filename = file.filename or ""

    try:
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=415,
                detail="Please upload a PDF file.",
            )

        await validate_upload_size(file)

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty.",
            )

        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=415,
                detail="The uploaded file is not a valid PDF.",
            )

        page_numbers = []

        try:
            for part in pages.split(","):
                part = part.strip()

                if not part:
                    raise ValueError(
                        "Enter page numbers like 1,3,5 or 2-5."
                    )

                if "-" in part:
                    range_parts = part.split("-")

                    if len(range_parts) != 2:
                        raise ValueError(
                            "Invalid page range. Use a format like 2-5."
                        )

                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())

                    if start > end:
                        raise ValueError(
                            "Page range start must not exceed its end."
                        )

                    if start < 1:
                        raise ValueError(
                            "Page numbers must start from 1."
                        )

                    page_numbers.extend(range(start, end + 1))

                else:
                    page_numbers.append(int(part))

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=(
                    str(exc)
                    if str(exc).startswith(
                        (
                            "Enter page numbers",
                            "Invalid page range",
                            "Page range start",
                            "Page numbers",
                        )
                    )
                    else "Invalid page selection. Use 1,3,5 or 2-5."
                ),
            ) from exc

        extracted_pdf = extract_pdf_pages(
            content,
            page_numbers,
        )

        return StreamingResponse(
            BytesIO(extracted_pdf),
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    'attachment; filename="nova-extracted-pages.pdf"'
                ),
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
            },
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()


@router.post("/tools/rotate-pdf", tags=["PDF Tools"])
async def rotate_pdf_endpoint(
    file: UploadFile=File(
        ...,
        description="Upload a PDF file to rotate.",
    ),
    rotation: int=Form(
        ...,
        description="Clockwise rotation: 90, 180, or 270 degrees.",
    ),
    pages: str | None=Form(
        default=None,
        description="Optional page numbers, e.g. 1,3 or 2-4. "
                    "Leave empty to rotate all pages.",
    ),
):
    """Rotate all PDF pages or selected pages."""

    filename = file.filename or ""

    try:
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=415,
                detail="Please upload a PDF file.",
            )

        await validate_upload_size(file)

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty.",
            )

        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=415,
                detail="The uploaded file is not a valid PDF.",
            )

        if rotation not in {90, 180, 270}:
            raise HTTPException(
                status_code=400,
                detail="Rotation must be 90, 180, or 270 degrees.",
            )

        page_numbers = None

        if pages is not None and pages.strip():
            page_numbers = []

            try:
                for part in pages.split(","):
                    part = part.strip()

                    if not part:
                        raise ValueError(
                            "Enter page numbers like 1,3 or 2-4."
                        )

                    if "-" in part:
                        range_parts = part.split("-")

                        if len(range_parts) != 2:
                            raise ValueError(
                                "Invalid page range. Use a format like 2-4."
                            )

                        start = int(range_parts[0].strip())
                        end = int(range_parts[1].strip())

                        if start > end:
                            raise ValueError(
                                "Page range start must not exceed its end."
                            )

                        if start < 1:
                            raise ValueError(
                                "Page numbers must start from 1."
                            )

                        page_numbers.extend(range(start, end + 1))

                    else:
                        page_numbers.append(int(part))

            except ValueError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        str(exc)
                        if str(exc).startswith(
                            (
                                "Enter page numbers",
                                "Invalid page range",
                                "Page range start",
                                "Page numbers",
                            )
                        )
                        else "Invalid page selection. Use 1,3 or 2-4."
                    ),
                ) from exc

        rotated_pdf = rotate_pdf(
            content,
            rotation,
            page_numbers,
        )

        return StreamingResponse(
            BytesIO(rotated_pdf),
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    'attachment; filename="nova-rotated.pdf"'
                ),
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
            },
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()


@router.post(
    "/extract-text",
    response_class=PlainTextResponse,
    summary="Extract Text from PDF",
    description="Extract selectable text from an uploaded PDF. OCR is not supported.",
)
async def extract_text_from_pdf_endpoint(
    file: UploadFile=File(..., description="PDF file to extract text from"),
):
    try:
                # Validate the uploaded file's extension.
        validate_extension(
            file.filename,
            ALLOWED_PDF_EXTENSIONS,
        )

        # Validate the uploaded file's size.
        await validate_upload_size(file)

        # Read the uploaded PDF.
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty.",
            )

        # Extract text using the service.
        extracted_text = extract_text_from_pdf(content)

        return PlainTextResponse(
            content=extracted_text,
            headers={
                "Content-Disposition": 'attachment; filename="nova-extracted-text.txt"'
            },
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()

