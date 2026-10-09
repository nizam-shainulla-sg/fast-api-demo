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
