# P1 — Frontend Foundation Decision and Starter

**Status:** Starter scaffold created; install and run locally to verify.

## P1.1 Project setup
- Vite + React + TypeScript.
- npm scripts for development and production build.
- Environment variable `VITE_API_BASE_URL` reserved for the FastAPI backend.

## P1.2 Routing and shared layout
- React Router.
- Shared header/sidebar-style navigation and responsive content area.
- Dedicated routes for each MVP tool.

## P1.3 Dashboard and tool cards
- Dashboard presents the five MVP workflows.
- Cards navigate to dedicated pages.

## P1.4 Responsive design
- CSS grid adapts to mobile and desktop.
- Keyboard-visible focus states and reduced-motion-friendly styling.

## Scope boundary
This is the frontend foundation and UI wiring only. File-processing API endpoints will be implemented in the backend phase. Tool pages show an explicit API-not-connected state until the backend is ready; they do not pretend to process files locally.

## Run
1. Install Node.js LTS.
2. Open a terminal in `frontend`.
3. Run `npm install`.
4. Run `npm run dev`.
5. Set `VITE_API_BASE_URL` in `.env` when the backend is available.
