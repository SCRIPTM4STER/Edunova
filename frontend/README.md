# EduNova Frontend (React + Vite)

A backend-aligned frontend for this repository's Django REST API.

## Implemented backend coverage

- **Auth**
  - `POST /api/v1/auth/token/`
  - `POST /api/v1/auth/token/refresh/`
  - `POST /api/v1/auth/register/`
  - `POST /api/v1/auth/google/` (Google token submit flow)
  - `GET /api/v1/auth/profile/me/`
  - `POST /api/v1/auth/change-password/`
- **Notebook/Note**
  - `GET/POST /api/v1/notebook/notebooks/`
  - `GET/POST /api/v1/notebook/notes/`
  - `GET/PATCH/DELETE /api/v1/notebook/notes/:id/`
  - `POST /api/v1/notebook/notes/:id/generate-pdf/`
- **PDF**
  - `GET /api/v1/pdf/`
  - `POST /api/v1/pdf/upload/`
  - `GET/PATCH/DELETE /api/v1/pdf/:id/`
  - `GET /api/v1/pdf/:id/download/`

## Stack

- React 18 + Vite
- React Router 6
- Axios
- Minimal custom CSS

## Project structure

```text
frontend/
  src/
    api/              # Backend-domain API methods + axios clients
    components/       # Reusable UI components (alerts, pagination, loaders)
    contexts/         # Auth session state + bootstrap
    hooks/            # Async action helper
    layouts/          # Authenticated app shell
    pages/            # Route-level features: auth, dashboard, notes, pdf, profile
    styles/           # Global styles
    utils/            # Token storage utilities
```

## Key behavior

- JWT access token is automatically attached to API calls.
- On `401`, the client attempts refresh using the stored refresh token and retries pending requests.
- Notes and PDFs support pagination controls against DRF paginated responses.
- Note create/edit supports optional image upload (`multipart/form-data`).
- PDF upload/edit supports file and cover image upload (`multipart/form-data`) plus linked note selection.
- Profile page reads all exposed profile fields from backend.

## Important backend limitations reflected in UI

- Profile endpoint in backend is currently **GET-only** (`RetrieveAPIView`), so profile editing is intentionally not included.
- Password change requires backend-managed session flag `reauth_verified`; UI surfaces backend error message when not satisfied.

## Environment

Copy env file:

```bash
cp .env.example .env
```

Set API URL:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Run locally

```bash
cd frontend
npm install
npm run dev
```

Default app URL: `http://localhost:3000`
