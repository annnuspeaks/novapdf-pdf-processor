# Nexora PDF Tools — Master Development Checklist

**Version:** 1.0  
**Target:** 2–3 days  
**Budget:** ₹0 for software and AI APIs  
**Platform:** Web first; architecture should support future Android integration  
**Status:** P0 — Project Decisions & Documentation

> Mark items `[x]` only after they are completed and verified. This checklist is the single source of truth.

## P0 — Decisions & Documentation

- [ ] **P0.1 Project-level decisions**
  - [ ] P0.1.1 Finalize project name and purpose
  - [ ] P0.1.2 Define MVP scope and exclusions
  - [ ] P0.1.3 Confirm free/open-source-only approach; no paid APIs
  - [ ] P0.1.4 Choose lightweight web-first architecture
  - [ ] P0.1.5 Define future Android integration approach
  - [ ] P0.1.6 Confirm 2–3 day delivery target
- [ ] **P0.2 Documentation template**
  - [ ] P0.2.1 Create one concise decision document per tool
  - [ ] P0.2.2 Include: decision, purpose, scope, input, processing, output, technology, AI need, dependencies, limitations, acceptance criteria
- [ ] **P0.3 Tool decisions**
  - [ ] P0.3.1 Images to PDF
  - [ ] P0.3.2 PDF to Images
  - [ ] P0.3.3 Word to PDF
  - [ ] P0.3.4 Excel to PDF
  - [ ] P0.3.5 PowerPoint to PDF
  - [ ] P0.3.6 TXT to PDF
  - [ ] P0.3.7 Merge PDFs
  - [ ] P0.3.8 Split PDF
  - [ ] P0.3.9 Extract PDF Pages
  - [ ] P0.3.10 Rotate PDF Pages
  - [ ] P0.3.11 Reorder PDF Pages
  - [ ] P0.3.12 Delete PDF Pages
  - [ ] P0.3.13 Compress PDF
  - [ ] P0.3.14 Add Page Numbers
  - [ ] P0.3.15 Add Watermark
  - [ ] P0.3.16 Extract Text from PDF
  - [ ] P0.3.17 Extract Images from PDF
  - [ ] P0.3.18 AI PDF Summarizer (optional; lightweight local model only if practical)
  - [ ] P0.3.19 Chat with PDF (optional; lightweight local model only if practical)
  - [ ] P0.3.20 PDF Information Extractor (optional; distinguish rule-based extraction from AI)
- [ ] **P0.4 MVP priority**
  - [ ] P0.4.1 Lock must-have tools for the 2–3 day release
  - [ ] P0.4.2 Mark time-consuming tools as post-MVP if needed
  - [ ] P0.4.3 Record unsupported hosting/runtime requirements

## P1 — Frontend Foundation

- [ ] **P1.1 Setup**
  - [ ] P1.1.1 Initialize frontend project
  - [ ] P1.1.2 Establish folder structure
  - [ ] P1.1.3 Configure routing
  - [ ] P1.1.4 Configure global styles and typography
  - [ ] P1.1.5 Create reusable components
- [ ] **P1.2 Nexora-inspired UI**
  - [ ] P1.2.1 Define color palette and design tokens
  - [ ] P1.2.2 Build navbar
  - [ ] P1.2.3 Build sidebar or compact navigation
  - [ ] P1.2.4 Build reusable tool cards
  - [ ] P1.2.5 Standardize icons, buttons, fields and cards
- [ ] **P1.3 Dashboard**
  - [ ] P1.3.1 Build dashboard landing page
  - [ ] P1.3.2 Group tools into categories
  - [ ] P1.3.3 Display approved tools as cards
  - [ ] P1.3.4 Link each card to its dedicated page
  - [ ] P1.3.5 Add search/filter if time permits
- [ ] **P1.4 Reusable tool page**
  - [ ] P1.4.1 Build dedicated tool page template
  - [ ] P1.4.2 Add file picker and drag-and-drop
  - [ ] P1.4.3 Add tool-specific input controls
  - [ ] P1.4.4 Add process button and loading state
  - [ ] P1.4.5 Show result/preview on the same page
  - [ ] P1.4.6 Add direct-download button
  - [ ] P1.4.7 Add validation, empty, success and error states
  - [ ] P1.4.8 Add reset/clear action
  - [ ] P1.4.9 Revoke temporary browser object URLs when no longer needed

## P2 — Backend Initiation

- [x] **P2.1 Setup**
  - [x] P2.1.1 Create Python virtual environment
  - [x] P2.1.2 Initialize FastAPI
  - [x] P2.1.3 Install and pin required dependencies
  - [x] P2.1.4 Configure environment settings
  - [x] P2.1.5 Establish API route and service structure
  - [x] P2.1.6 Configure CORS for development and production
  - [x] P2.1.7 Add health-check endpoint
- [ ] **P2.2 File pipeline**
  - [ ] P2.2.1 Implement upload handling
  - [ ] P2.2.2 Validate file type and extension
  - [ ] P2.2.3 Configure upload and resource limits
  - [ ] P2.2.4 Use isolated temporary directories per job
  - [ ] P2.2.5 Generate output files safely
  - [ ] P2.2.6 Implement download endpoint and filenames
  - [ ] P2.2.7 Clean up temporary input/output files
  - [ ] P2.2.8 Return clear, safe API errors
- [ ] **P2.3 Frontend integration**
  - [ ] P2.3.1 Configure API base URL
  - [ ] P2.3.2 Connect upload and processing requests
  - [ ] P2.3.3 Connect loading and error states
  - [ ] P2.3.4 Display result/preview on the same page
  - [ ] P2.3.5 Verify direct download to the browser's default Downloads location
  - [ ] P2.3.6 Test local end-to-end flow

## P3 — Individual Tool Implementation

**Shared completion steps for every tool:** processing logic → API/service integration → dedicated page integration → valid/invalid input tests → output verification → update tool decision document.

- [ ] **P3.1 Conversion tools**
  - [ ] P3.1.1 Images to PDF
  - [ ] P3.1.2 PDF to JPG/PNG
  - [ ] P3.1.3 TXT to PDF
  - [ ] P3.1.4 Word to PDF
  - [ ] P3.1.5 Excel to PDF
  - [ ] P3.1.6 PowerPoint to PDF
  - [ ] P3.1.7 Verify/document LibreOffice or other system dependency for Office conversions
- [ ] **P3.2 PDF organization tools**
  - [ ] P3.2.1 Merge PDFs
  - [ ] P3.2.2 Split PDF
  - [ ] P3.2.3 Extract selected pages
  - [ ] P3.2.4 Rotate pages
  - [ ] P3.2.5 Reorder pages
  - [ ] P3.2.6 Delete selected pages
- [ ] **P3.3 Optimization and editing**
  - [ ] P3.3.1 Compress PDF
  - [ ] P3.3.2 Add page numbers
  - [ ] P3.3.3 Add watermark
  - [ ] P3.3.4 Extract text
  - [ ] P3.3.5 Extract images
- [ ] **P3.4 Optional AI-assisted tools**
  - [ ] P3.4.1 Evaluate a lightweight local model/runtime
  - [ ] P3.4.2 PDF summarizer
  - [ ] P3.4.3 Chat with PDF
  - [ ] P3.4.4 PDF information extractor
  - [ ] P3.4.5 Keep AI optional; no paid API or heavyweight hosted model
  - [ ] P3.4.6 If local AI is impractical within the deadline, defer it and document why
  - [ ] P3.4.7 Do not label rule-based functionality as AI

## P4 — UI Fixes & Polish

- [ ] **P4.1 Functional testing**
  - [ ] P4.1.1 Test every implemented tool's success path
  - [ ] P4.1.2 Test unsupported and malformed files
  - [ ] P4.1.3 Test empty inputs and invalid page ranges
  - [ ] P4.1.4 Test processing failures and oversized files
  - [ ] P4.1.5 Verify output opens and content is correct
  - [ ] P4.1.6 Verify download filename and file integrity
- [ ] **P4.2 UI polish**
  - [ ] P4.2.1 Fix dashboard spacing and alignment
  - [ ] P4.2.2 Make cards and tool pages visually consistent
  - [ ] P4.2.3 Polish forms, buttons and icons
  - [ ] P4.2.4 Polish loading, success and error states
  - [ ] P4.2.5 Verify preview and download flow
- [ ] **P4.3 Responsive checks**
  - [ ] P4.3.1 Verify desktop layout
  - [ ] P4.3.2 Verify tablet layout
  - [ ] P4.3.3 Verify mobile layout
  - [ ] P4.3.4 Fix navigation, overflow and scrolling
  - [ ] P4.3.5 Verify touch targets and file selection

## P5 — Deployment

- [ ] **P5.1 Preparation**
  - [ ] P5.1.1 Create production frontend build
  - [ ] P5.1.2 Configure production backend startup
  - [ ] P5.1.3 Set production API URL and allowed origins
  - [ ] P5.1.4 Document Python/system dependencies
  - [ ] P5.1.5 Verify file security and cleanup
  - [ ] P5.1.6 Check free-host file size, memory, timeout and storage limits
- [ ] **P5.2 Hosting**
  - [ ] P5.2.1 Select a suitable free frontend host
  - [ ] P5.2.2 Select a suitable free backend host, if needed
  - [ ] P5.2.3 Deploy frontend
  - [ ] P5.2.4 Deploy backend
  - [ ] P5.2.5 Configure frontend/backend connection
- [ ] **P5.3 Live verification**
  - [ ] P5.3.1 Verify dashboard and routes
  - [ ] P5.3.2 Verify uploads and processing
  - [ ] P5.3.3 Verify output and downloads
  - [ ] P5.3.4 Verify error handling and temporary-file cleanup
  - [ ] P5.3.5 Record free-host limitations

## P6 — Release & Documentation

- [ ] **P6.1 Project documentation**
  - [ ] P6.1.1 Write master README
  - [ ] P6.1.2 Document project overview and feature list
  - [ ] P6.1.3 Document technology stack and architecture
  - [ ] P6.1.4 Document prerequisites and installation
  - [ ] P6.1.5 Document frontend startup
  - [ ] P6.1.6 Document backend startup
  - [ ] P6.1.7 Document environment configuration
  - [ ] P6.1.8 Document supported formats and tool limitations
  - [ ] P6.1.9 Document AI approach and limitations
  - [ ] P6.1.10 Document deployment and known hosting constraints
- [ ] **P6.2 Tool documentation**
  - [ ] P6.2.1 Update each implemented tool's decision document
  - [ ] P6.2.2 Verify input, processing and output descriptions
  - [ ] P6.2.3 Record dependencies and limitations
  - [ ] P6.2.4 Mark deferred tools clearly
- [ ] **P6.3 Release**
  - [ ] P6.3.1 Run final regression test
  - [ ] P6.3.2 Complete final UI review
  - [ ] P6.3.3 Remove temporary files and unused code
  - [ ] P6.3.4 Verify `.gitignore` and secret handling
  - [ ] P6.3.5 Tag release version
  - [ ] P6.3.6 Record live URL
  - [ ] P6.3.7 Record future Android integration notes

## Day-wise Target

- [ ] **Day 1:** P0 decisions, P1 frontend foundation, P2 backend pipeline
- [ ] **Day 2:** P3 core PDF tools and end-to-end integration
- [ ] **Day 3:** P4 polish/testing, P5 deployment, P6 release/docs

## Master Status

| Phase | Name | Status |
|---|---|---|
| P0 | Decisions & Documentation | Not started |
| P1 | Frontend Foundation | Not started |
| P2 | Backend Initiation | Not started |
| P3 | Individual Tool Implementation | Not started |
| P4 | UI Fixes & Polish | Not started |
| P5 | Deployment | Not started |
| P6 | Release & Documentation | Not started |

**Current phase:** P0 — Decisions & Documentation  
**Completed phases:** None  
**Release rule:** A tool is complete only after processing, UI integration, output validation and download have been tested.
