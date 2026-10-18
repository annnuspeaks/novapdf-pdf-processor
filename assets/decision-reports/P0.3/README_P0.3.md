# Nexora PDF Tools — P0.3 Individual Tool Decision Reports

**Status:** Initial decision drafts created. Each report must be validated against implementation and dependency licensing before being marked approved.

## Reports
- [ ] `P0.3.01_Images_to_PDF.md` — Images to PDF
- [ ] `P0.3.02_PDF_to_Images.md` — PDF to Images
- [ ] `P0.3.03_Word_to_PDF.md` — Word to PDF
- [ ] `P0.3.04_Excel_to_PDF.md` — Excel to PDF
- [ ] `P0.3.05_PowerPoint_to_PDF.md` — PowerPoint to PDF
- [ ] `P0.3.06_TXT_to_PDF.md` — TXT to PDF
- [ ] `P0.3.07_Merge_PDFs.md` — Merge PDFs
- [ ] `P0.3.08_Split_PDF.md` — Split PDF
- [ ] `P0.3.09_Extract_PDF_Pages.md` — Extract PDF Pages
- [ ] `P0.3.10_Rotate_PDF_Pages.md` — Rotate PDF Pages
- [ ] `P0.3.11_Reorder_PDF_Pages.md` — Reorder PDF Pages
- [ ] `P0.3.12_Delete_PDF_Pages.md` — Delete PDF Pages
- [ ] `P0.3.13_Compress_PDF.md` — Compress PDF
- [ ] `P0.3.14_Add_Page_Numbers.md` — Add Page Numbers
- [ ] `P0.3.15_Add_Watermark.md` — Add Watermark
- [ ] `P0.3.16_Extract_Text_from_PDF.md` — Extract Text from PDF
- [ ] `P0.3.17_Extract_Images_from_PDF.md` — Extract Images from PDF
- [ ] `P0.3.18_AI_PDF_Summarizer.md` — AI PDF Summarizer
- [ ] `P0.3.19_Chat_with_PDF.md` — Chat with PDF
- [ ] `P0.3.20_PDF_Information_Extractor.md` — PDF Information Extractor

## Project rules
- Free/open-source-only; no paid APIs.
- Keep the user workflow on one dedicated tool page: input → process → result → direct download.
- Use React + Vite and FastAPI as the default web stack.
- Prefer pypdf and Pillow for simple workflows; introduce heavier/system dependencies only when needed.
- Treat LibreOffice conversions as conditional on installed system dependencies and deployment support.
- Review PyMuPDF/AGPL implications before deployment; do not assume every open-source license is interchangeable.
- AI summarizer and Chat with PDF are deferred until local-model feasibility, hardware, and licensing are confirmed.
- The 2–3 day target is for a limited MVP, not all listed tools.

## Suggested storage location
`D:\MCA PU\Semesters\Semester 3\MCA_Projects\Nexora-Co_brands\nexora_pdf_tool\decision-reports\P0.3\`
