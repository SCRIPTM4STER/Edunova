# EduNova Frontend (React + Vite)

This frontend is built directly against the Django DRF backend in this repository.
It covers:

- JWT authentication (`/api/v1/auth/token/`, refresh, register, profile)
- Notebook creation/listing
- Note creation/listing/deletion and PDF generation from notes
- PDF upload/list/download/delete

## Stack

- React 18
- Vite 5
- React Router 6
- Axios
- Plain CSS (minimal clean UI)

## Project Structure

```text
frontend/
  src/
    api/              # Axios client + endpoint modules by domain
    components/       # Reusable UI building blocks
    contexts/         # Auth context + session bootstrap
    hooks/            # Shared async/loading/error helper hooks
    layouts/          # App shell layout for authenticated routes
    pages/            # Route-level pages (auth, notes, PDFs, profile)
    styles/           # Global styling
    utils/            # Token storage helper
```

## Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set backend API base URL:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Run locally

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000` (matches backend README CSRF trusted origins defaults).

## Notes about backend behavior

- Access token expiry is 5 minutes; frontend automatically refreshes using refresh token on `401`.
- Change password endpoint requires backend session flag (`reauth_verified`) before allowing updates.
- Many list endpoints are paginated (`count/results/next/previous`) and handled as such in notes/PDF pages.
- File upload uses multipart/form-data and supports PDF file restrictions defined by backend.
