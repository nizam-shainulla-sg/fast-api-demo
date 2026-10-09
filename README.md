# Patient API

A small FastAPI app that stores patient details in a SQLite database.

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | App entry point; initialises the DB on startup and includes routers |
| `database.py` | SQLite connection, table creation and sample data |
| `patients.py` | Patient endpoints (`/patients`) |
| `test.py` | Sample router with four demo routes (`/test`) |
| `patients.db` | SQLite database file (created automatically on first run) |

## Setup

```bash
python3 -m venv .my_venv
source .my_venv/bin/activate
pip install fastapi uvicorn
```

## Run

```bash
uvicorn main:app --reload
```

The API runs at http://127.0.0.1:8000. Interactive docs are at http://127.0.0.1:8000/docs.

## Database

On startup, `patients.db` is created with a `patients` table and one sample patient if the table is empty.

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key, auto-increment |
| `name` | TEXT | Required |
| `age` | INTEGER | Required |
| `gender` | TEXT | Required |
| `phone` | TEXT | Optional |
| `diagnosis` | TEXT | Optional |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/patients/` | Create a patient (returns 201) |
| GET | `/patients/` | List all patients |
| GET | `/patients/{patient_id}` | Get one patient (404 if not found) |
| DELETE | `/patients/{patient_id}` | Delete a patient (404 if not found) |

### Example

```bash
curl -X POST http://127.0.0.1:8000/patients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "age": 30, "gender": "female", "phone": "555-0101", "diagnosis": "Asthma"}'
```

```json
{
  "id": 2,
  "name": "Jane Doe",
  "age": 30,
  "gender": "female",
  "phone": "555-0101",
  "diagnosis": "Asthma"
}
```

## Note

`test.py` is not included in `main.py`, so its routes are inactive. To enable them, add `from test import router as test_router` and `app.include_router(test_router)` to `main.py`. The name `test` clashes with Python's standard library module, so you may prefer to rename the file.

## Authentication

All `/patients` endpoints require an API key sent in the `X-API-Key` header. `/`, `/docs` and `/openapi.json` stay public.

The server reads the expected key from the `API_KEY` environment variable. If it is not set, the protected endpoints return 503 instead of running unprotected.

Generate a key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run locally with it:

```bash
API_KEY=your-key uvicorn main:app --reload
curl -H "X-API-Key: your-key" http://127.0.0.1:8000/patients/
```

In `/docs`, click **Authorize** and paste the key to try the endpoints.

| Case | Status |
|------|--------|
| Missing or wrong key | 401 |
| `API_KEY` not configured on the server | 503 |

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests use a temporary SQLite file, so `patients.db` is never touched.

## Deploy to Railway

1. Push this repo to GitHub.
2. On https://railway.com choose **New Project → Deploy from GitHub repo** and pick this repo.
3. Railway reads `requirements.txt` and `railway.json` and starts `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. In the service, open **Settings → Networking → Generate Domain** to get a public URL. Docs are at `<url>/docs`.

### Keeping data between deploys

Railway's container disk is wiped on every deploy. To keep the SQLite file:

1. Add a **Volume** to the service, mounted at `/data`.
2. Set the variable `DB_PATH=/data/patients.db`.

### Required variable

Set `API_KEY` in the service's **Variables** tab before using `/patients`.

For real production use, move to managed Postgres instead (see the notes on databases).
