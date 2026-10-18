from io import BytesIO

import pytest
from PIL import Image
from pypdf import PdfReader, PdfWriter

from app.services.pdf_service import images_to_pdf
from app.services.merge_service import merge_pdfs
from app.services.split_service import extract_pdf_pages
from app.services.rotate_service import rotate_pdf
from app.services.extract_text_service import extract_text_from_pdf


def create_pdf(texts=None):
    """Create a small in-memory PDF for testing."""
    writer = PdfWriter()

    for text in texts or ["Test page"]:
        page = writer.add_blank_page(width=300, height=300)

        # Blank pages are sufficient for page-count and rotation tests.
        # Text extraction tests use a separate fixture below.

    output = BytesIO()
    writer.write(output)
    writer.close()
    return output.getvalue()


def create_image(format="PNG"):
    """Create a small in-memory image."""
    image = Image.new("RGB", (20, 20), "white")
    output = BytesIO()
    image.save(output, format=format)
    image.close()
    return output.getvalue()


def get_pdf_page_count(content):
    reader = PdfReader(BytesIO(content))
    return len(reader.pages)


# ---------- Images to PDF ----------

def test_images_to_pdf_creates_pdf():
    result = images_to_pdf([create_image("PNG")])

    assert result.startswith(b"%PDF-")
    assert get_pdf_page_count(result) == 1


def test_images_to_pdf_rejects_empty_list():
    with pytest.raises(ValueError):
        images_to_pdf([])


def test_images_to_pdf_rejects_invalid_image():
    with pytest.raises(ValueError):
        images_to_pdf([b"not an image"])


# ---------- Merge PDFs ----------

def test_merge_pdfs_creates_combined_pdf():
    result = merge_pdfs([
        create_pdf(["Page 1"]),
        create_pdf(["Page 2"]),
    ])

    assert result.startswith(b"%PDF-")
    assert get_pdf_page_count(result) == 2


def test_merge_pdfs_rejects_single_pdf():
    with pytest.raises(ValueError):
        merge_pdfs([create_pdf()])


def test_merge_pdfs_rejects_invalid_pdf():
    with pytest.raises(ValueError):
        merge_pdfs([
            create_pdf(),
            b"not a PDF",
        ])


# ---------- Extract PDF Pages ----------

def test_extract_pdf_pages_selects_requested_pages():
    source = create_pdf(["Page 1", "Page 2", "Page 3"])

    result = extract_pdf_pages(source, [1, 3])

    assert result.startswith(b"%PDF-")
    assert get_pdf_page_count(result) == 2


def test_extract_pdf_pages_rejects_out_of_range_page():
    with pytest.raises(ValueError):
        extract_pdf_pages(create_pdf(), [2])


def test_extract_pdf_pages_rejects_duplicate_pages():
    with pytest.raises(ValueError):
        extract_pdf_pages(create_pdf(), [1, 1])


# ---------- Rotate PDF ----------

def test_rotate_pdf_preserves_page_count():
    source = create_pdf(["Page 1", "Page 2"])

    result = rotate_pdf(source, 90)

    assert result.startswith(b"%PDF-")
    assert get_pdf_page_count(result) == 2


def test_rotate_pdf_rejects_invalid_rotation():
    with pytest.raises(ValueError):
        rotate_pdf(create_pdf(), 45)


def test_rotate_pdf_rejects_out_of_range_page():
    with pytest.raises(ValueError):
        rotate_pdf(create_pdf(), 90, [2])


# ---------- Extract Text ----------

def test_extract_text_rejects_empty_pdf():
    with pytest.raises(ValueError, match="empty"):
        extract_text_from_pdf(b"")


def test_extract_text_rejects_invalid_pdf():
    with pytest.raises(ValueError):
        extract_text_from_pdf(b"not a PDF")


def test_extract_text_rejects_pdf_without_selectable_text():
    with pytest.raises(ValueError, match="No selectable text"):
        extract_text_from_pdf(create_pdf())