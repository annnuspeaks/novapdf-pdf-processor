from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract selectable text from a PDF without using OCR."""

    if not pdf_content:
        raise ValueError("The uploaded PDF is empty.")

    if not pdf_content.startswith(b"%PDF-"):
        raise ValueError("The uploaded file is not a valid PDF.")

    try:
        reader = PdfReader(BytesIO(pdf_content), strict=True)

        if reader.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        if len(reader.pages) == 0:
            raise ValueError("The PDF does not contain any pages.")

        extracted_pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            extracted_pages.append(
                f"--- Page {page_number} ---\n{text.strip()}"
            )

        extracted_text = "\n\n".join(extracted_pages)

        if not any(
            (page.extract_text() or "").strip()
            for page in reader.pages
        ):
            raise ValueError(
                "No selectable text was found in this PDF. "
                "It may be a scanned document. OCR is not supported yet."
            )

        return extracted_text

    except PdfReadError as exc:
        raise ValueError(
            "The uploaded PDF is corrupted or cannot be read."
        ) from exc

    except (OSError, KeyError, IndexError) as exc:
        raise ValueError(
            "The PDF is corrupted or cannot be processed."
        ) from exc