<p align="center">
  <img src="assets/branding/nexora-logo.png" alt="Nexora — Enterprise Decision Intelligence System" width="820">
</p>

<h1 align="center">NOVA PDF Tools</h1>

<p align="center">
  <img src="assets/branding/nova-pdf-logo.png" alt="NOVA PDF" width="620">
  <br>
  <strong>A free PDF-processing workspace built under the Nexora ecosystem.</strong>
</p>

<p align="center">
  <a href="https://github.com/annnuspeaks/novapdf-pdf-processor"><img alt="Repository" src="https://img.shields.io/badge/repository-public-brightgreen"></a>
  <img alt="Backend" src="https://img.shields.io/badge/backend-FastAPI-009688">
  <img alt="Frontend" src="https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
</p>

> **Product relationship:** Nexora is the parent ecosystem. **NOVA PDF Tools** is an independent utility product within that ecosystem; this repository documents and contains the NOVA PDF processor.

## Overview

NOVA PDF Tools is a web-based utility for common PDF and image-processing tasks. It pairs a React + Vite interface with a FastAPI backend that validates uploaded files and returns processed documents.

## Features

- **Images to PDF** — convert JPEG/JPG and PNG images into a PDF.
- **Merge PDFs** — combine multiple PDF files in their selected order.
- **Split / Extract Pages** — extract selected pages or page ranges into a new PDF.
- **Rotate PDF Pages** — rotate PDF pages by supported 90-degree increments.
- **Extract Text** — export selectable text from a PDF as plain text. **OCR for scanned/image-only PDFs is not supported.**
- **API safeguards** — upload validation, request-size limits, CORS configuration, security headers, and automated tests.

## Technology

| Layer | Stack |
|---|---|
| Frontend | React, TypeScript, Vite, React Router |
| Backend | Python, FastAPI, Uvicorn, Pydantic Settings |
| PDF and image processing | pypdf, Pillow |
| Tests | pytest, FastAPI TestClient, httpx |

## Project structure

```text
novapdf-pdf-processor/
├── assets/
│   └── branding/          # Nexora parent and NOVA PDF logos
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routes
│   │   ├── services/       # PDF processing logic
│   │   ├── utils/          # Upload validation
│   │   ├── config.py
│   │   ├── main.py
│   │   └── request_limits.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── public/images/
│   ├── src/
│   ├── package.json
│   └── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Run locally

### 1. Backend

From the repository root, create and activate a virtual environment if you do not already have one:

```bash
cd backend
python -m venv .venv
```

Windows CMD:

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

**Backend environment:** `.env` is optional for local development because defaults are defined in `backend/app/config.py`. Create `backend/.env` only when you need to override settings. Never commit `.env` files or secrets.

### 2. Frontend

Open a second terminal:

```cmd
cd frontend
npm install
```

Create `frontend/.env` from `.env.example` if needed. The example sets:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```cmd
npm run dev
```

Open the local URL printed by Vite.

> **Integration status:** the backend processing endpoints and tests are implemented. The frontend workspace is present; connecting each tool's upload, form, API request, loading/error handling, and result download flow is the next integration step. Endpoint paths and request fields must match the backend routes below.

## API endpoints

Base URL for local development: `http://127.0.0.1:8000`

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | API welcome response |
| `GET` | `/api/health` | Health check |
| `POST` | `/api/tools/images-to-pdf` | Convert uploaded images to PDF (`files`) |
| `POST` | `/api/tools/merge-pdfs` | Merge PDFs (`files`, at least 2) |
| `POST` | `/api/tools/extract-pages` | Extract page numbers/ranges (`file`, `pages`) |
| `POST` | `/api/tools/rotate-pdf` | Rotate PDF pages (see Swagger for fields) |
| `POST` | `/api/extract-text` | Extract selectable text (`file`) |

See `/docs` for the exact request fields, validation rules, and response details.

## Tests

Run the complete backend test suite from the repository root:

```cmd
python -m pytest backend/tests -v
```

**Latest verified result:** 35 tests passed, 0 failed. One Starlette deprecation warning about `httpx` and `TestClient` was present; it did not fail the suite.

## Security notes

- Keep `.env`, credentials, private keys, virtual environments, `node_modules`, build output, and caches out of version control.
- Uploaded files are subject to configured upload and request-size limits.
- Do not deploy with development settings unchanged; configure trusted frontend origins and production server/proxy limits before deployment.
- This project is a file-processing utility, not an OCR system.

## License

Distributed under the [MIT License](LICENSE).
