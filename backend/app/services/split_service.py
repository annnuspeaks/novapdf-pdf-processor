from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def extract_pdf_pages(
    pdf_content: bytes,
    page_numbers: list[int],
) -> bytes:
    """
    Extract selected pages from a PDF.

    Page numbers are 1-based.
    Example: [1, 3, 5]
    """

    if not pdf_content:
        raise ValueError("The uploaded PDF is empty.")

    if not pdf_content.startswith(b"%PDF-"):
        raise ValueError("The uploaded file is not a valid PDF.")

    if not page_numbers:
        raise ValueError("Select at least one page to extract.")

    if any(page < 1 for page in page_numbers):
        raise ValueError("Page numbers must start from 1.")

    if len(set(page_numbers)) != len(page_numbers):
        raise ValueError("Duplicate page numbers are not allowed.")

    try:
        reader = PdfReader(BytesIO(pdf_content), strict=True)

        if reader.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        total_pages = len(reader.pages)

        if total_pages == 0:
            raise ValueError("The PDF does not contain any pages.")

        invalid_pages = [
            page for page in page_numbers
            if page > total_pages
        ]

        if invalid_pages:
            raise ValueError(
                f"Page numbers {invalid_pages} are out of range. "
                f"The PDF contains {total_pages} pages."
            )

        writer = PdfWriter()

        try:
            for page_number in page_numbers:
                writer.add_page(reader.pages[page_number - 1])

            output = BytesIO()
            writer.write(output)

            return output.getvalue()

        finally:
            writer.close()

    except PdfReadError as exc:
        raise ValueError(
            "The uploaded PDF is corrupted or cannot be read."
        ) from exc