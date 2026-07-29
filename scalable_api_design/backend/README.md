# Scalable API Backend

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Environment note

This backend should be installed in a dedicated virtual environment.

If you install these dependencies into a shared environment that already contains `streamlit`, `pip` may warn about `starlette` and `python-multipart` version conflicts. That warning is caused by the shared environment, not by this backend itself. A clean virtual environment avoids that cross-project package interference.

## Test health

```bash
curl http://localhost:8000/health
```

## Project structure

```
backend/
├── app/
│   ├── main.py              # App entrypoint
│   ├── api/routes/          # HTTP endpoints
│   ├── core/                # Config, logger, exceptions
│   ├── schemas/             # Request/response models
│   ├── services/            # Business logic
│   ├── storage/             # S3, DB, Redis adapters
│   ├── workers/             # Async job processors
│   └── observability/       # Metrics, tracing
├── tests/
├── scripts/
├── infra/terraform/
└── requirements.txt
```
