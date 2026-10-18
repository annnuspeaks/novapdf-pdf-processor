from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from pypdf import PdfReader, PdfWriter

from app.main import app

client = TestClient(app)

# ---------- Test Helpers ----------


def create_pdf(page_count=2):
    """Create a valid PDF with the requested number of blank pages."""
    writer = PdfWriter()

    for _ in range(page_count):
        writer.add_blank_page(width=300, height=300)

    output = BytesIO()
    writer.write(output)
    writer.close()

    return output.getvalue()


def create_image(format="PNG"):
    """Create a small valid image for API tests."""
    image = Image.new("RGB", (20, 20), "white")
    output = BytesIO()
    image.save(output, format=format)
    image.close()

    return output.getvalue()


def get_pdf_page_count(content):
    """Return the number of pages in a PDF."""
    reader = PdfReader(BytesIO(content))
    return len(reader.pages)

# ---------- Health Endpoint ----------


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ---------- Images to PDF API ----------


def test_images_to_pdf_endpoint():
    response = client.post(
        "/api/tools/images-to-pdf",
        files=[
            ("files", ("image1.png", create_image(), "image/png")),
            ("files", ("image2.png", create_image(), "image/png")),
        ],
    )

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF-")
    assert get_pdf_page_count(response.content) == 2
    assert "application/pdf" in response.headers["content-type"]


def test_images_to_pdf_rejects_missing_files():
    response = client.post("/api/tools/images-to-pdf")

    assert response.status_code == 422

# ---------- Merge PDFs API ----------


def test_merge_pdfs_endpoint():
    response = client.post(
        "/api/tools/merge-pdfs",
        files=[
            ("files", ("first.pdf", create_pdf(2), "application/pdf")),
            ("files", ("second.pdf", create_pdf(3), "application/pdf")),
        ],
    )

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF-")
    assert get_pdf_page_count(response.content) == 5


def test_merge_pdfs_rejects_single_file():
    response = client.post(
        "/api/tools/merge-pdfs",
        files=[
            ("files", ("first.pdf", create_pdf(1), "application/pdf")),
        ],
    )

    assert response.status_code == 400

# ---------- Extract PDF Pages API ----------


def test_extract_pages_endpoint():
    response = client.post(
        "/api/tools/extract-pages",
        data={"pages": "1,3"},
        files={
            "file": ("source.pdf", create_pdf(3), "application/pdf"),
        },
    )

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF-")
    assert get_pdf_page_count(response.content) == 2


def test_extract_pages_rejects_out_of_range_page():
    response = client.post(
        "/api/tools/extract-pages",
        data={"pages": "5"},
        files={
            "file": ("source.pdf", create_pdf(2), "application/pdf"),
        },
    )

    assert response.status_code == 400

# ---------- Rotate PDF API ----------


def test_rotate_pdf_endpoint():
    response = client.post(
        "/api/tools/rotate-pdf",
        data={
            "rotation": "90",
            "pages": "1",
        },
        files={
            "file": ("source.pdf", create_pdf(2), "application/pdf"),
        },
    )

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF-")
    assert get_pdf_page_count(response.content) == 2


def test_rotate_pdf_rejects_invalid_rotation():
    response = client.post(
        "/api/tools/rotate-pdf",
        data={
            "rotation": "45",
            "pages": "1",
        },
        files={
            "file": ("source.pdf", create_pdf(2), "application/pdf"),
        },
    )

    assert response.status_code == 400

# ---------- Extract Text API ----------


def test_extract_text_rejects_pdf_without_selectable_text():
    response = client.post(
        "/api/extract-text",
        files={
            "file": ("source.pdf", create_pdf(1), "application/pdf"),
        },
    )

    assert response.status_code == 400
    assert "No selectable text" in response.text


def test_extract_text_rejects_invalid_pdf():
    response = client.post(
        "/api/extract-text",
        files={
            "file": ("invalid.pdf", b"not a valid PDF", "application/pdf"),
        },
    )

    assert response.status_code == 400

# ---------- Security Headers Tests ----------


def test_security_headers_on_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"


def test_security_headers_on_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"


def test_security_headers_on_pdf_response():
    response = client.post(
        "/api/tools/merge-pdfs",
        files=[
            ("files", ("first.pdf", create_pdf(1), "application/pdf")),
            ("files", ("second.pdf", create_pdf(1), "application/pdf")),
        ],
    )

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"


def test_request_size_limit_rejects_oversized_request():
    response = client.post(
        "/api/health",
        content=b"x" * (100 * 1024 * 1024 + 1),
        headers={"Content-Type": "application/octet-stream"},
    )

    assert response.status_code == 413
    assert "exceeds" in response.json()["detail"].lower()
