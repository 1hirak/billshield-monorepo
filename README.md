# BillShield UK — Monorepo

Full-stack monorepo for BillShield UK, a household bill support web app.

## Structure

```
billshield/          # Frontend — React + TypeScript + Vite
billshield-backend/  # Backend — Python FastAPI + SQLAlchemy + SQLite
```

## CI/CD

| Workflow | Trigger | Job |
|----------|---------|-----|
| `frontend-ci` | Push to `billshield/**` | typecheck → test → build |
| `backend-ci` | Push to `billshield-backend/**` | pytest |
| `deploy` | Push to `main` | SSH to EC2 → pull → docker compose up -d |

## Local Development

```bash
# Backend
cd billshield-backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload

# Frontend
cd billshield
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

Backend at http://localhost:8000, frontend at http://localhost:3000.

## Tests

```bash
# Backend — 49 pytest tests
cd billshield-backend && PYTHONPATH=src pytest

# Frontend — 95 vitest tests
cd billshield && npm test
```

## API Endpoints

All under `/api/v1`. See `/docs` for Swagger UI. Full list in backend README.

## License

MIT
