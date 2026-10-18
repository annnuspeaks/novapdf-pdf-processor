from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def merge_pdfs(pdf_contents: list[bytes]) -> bytes:
    """Merge multiple valid PDF files into one PDF."""

    if len(pdf_contents) < 2:
        raise ValueError("Upload at least two PDF files to merge.")

    writer = PdfWriter()
    readers = []

    try:
        for content in pdf_contents:
            if not content:
                raise ValueError("Empty PDF files are not supported.")

            try:
                reader = PdfReader(BytesIO(content), strict=True)

                if reader.is_encrypted:
                    raise ValueError(
                        "Password-protected PDFs are not supported."
                    )

                if len(reader.pages) == 0:
                    raise ValueError("A PDF contains no pages.")

                # Access pages to detect many malformed PDF structures.
                for page in reader.pages:
                    writer.add_page(page)

                readers.append(reader)

            except PdfReadError as exc:
                raise ValueError(
                    "One of the uploaded files is not a valid PDF."
                ) from exc

            except (OSError, KeyError, IndexError) as exc:
                raise ValueError(
                    "A PDF is corrupted or cannot be processed."
                ) from exc

        output = BytesIO()
        writer.write(output)

        return output.getvalue()

    finally:
        writer.close()