from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def rotate_pdf(
    pdf_content: bytes,
    rotation: int,
    page_numbers: list[int] | None = None,
) -> bytes:
    """Rotate all PDF pages or selected pages clockwise.

    Page numbers are 1-based.
    Supported rotations: 90, 180, 270 degrees.
    """

    if not pdf_content:
        raise ValueError("The uploaded PDF is empty.")

    if not pdf_content.startswith(b"%PDF-"):
        raise ValueError("The uploaded file is not a valid PDF.")

    if rotation not in {90, 180, 270}:
        raise ValueError("Rotation must be 90, 180, or 270 degrees.")

    try:
        reader = PdfReader(BytesIO(pdf_content), strict=True)

        if reader.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        total_pages = len(reader.pages)

        if total_pages == 0:
            raise ValueError("The PDF does not contain any pages.")

        if page_numbers is not None:
            if not page_numbers:
                raise ValueError("Select at least one page to rotate.")

            if any(page < 1 for page in page_numbers):
                raise ValueError("Page numbers must start from 1.")

            if len(set(page_numbers)) != len(page_numbers):
                raise ValueError("Duplicate page numbers are not allowed.")

            invalid_pages = [
                page for page in page_numbers
                if page > total_pages
            ]

            if invalid_pages:
                raise ValueError(
                    f"Page numbers {invalid_pages} are out of range. "
                    f"The PDF contains {total_pages} pages."
                )

            selected_pages = set(page_numbers)
        else:
            selected_pages = set(range(1, total_pages + 1))

        writer = PdfWriter()

        try:
            for page_index, page in enumerate(reader.pages, start=1):
                if page_index in selected_pages:
                    page.rotate(rotation)

                writer.add_page(page)

            output = BytesIO()
            writer.write(output)

            return output.getvalue()

        finally:
            writer.close()

    except PdfReadError as exc:
        raise ValueError(
            "The uploaded PDF is corrupted or cannot be read."
        ) from exc

    except (OSError, KeyError, IndexError) as exc:
        raise ValueError(
            "The PDF is corrupted or cannot be processed."
        ) from exc