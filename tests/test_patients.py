import pytest
from fastapi.testclient import TestClient

import database
from main import app

PATIENT = {
    "name": "Jane Doe",
    "age": 30,
    "gender": "female",
    "phone": "555-0101",
    "diagnosis": "Asthma",
}


API_KEY = "test-key"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setenv("API_KEY", API_KEY)
    with TestClient(app, headers={"X-API-Key": API_KEY}) as c:
        yield c


@pytest.fixture
def anon(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setenv("API_KEY", API_KEY)
    with TestClient(app) as c:
        yield c


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200


def test_seed_patient_exists(client):
    r = client.get("/patients/")
    assert r.status_code == 200
    assert [p["name"] for p in r.json()] == ["John Doe"]


def test_create_patient(client):
    r = client.post("/patients/", json=PATIENT)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert {k: body[k] for k in PATIENT} == PATIENT


def test_create_patient_optional_fields(client):
    r = client.post("/patients/", json={"name": "Bob", "age": 5, "gender": "male"})
    assert r.status_code == 201
    assert r.json()["phone"] is None
    assert r.json()["diagnosis"] is None


def test_create_patient_missing_required_field(client):
    r = client.post("/patients/", json={"name": "No Age", "gender": "male"})
    assert r.status_code == 422


def test_create_patient_wrong_type(client):
    r = client.post("/patients/", json={**PATIENT, "age": "abc"})
    assert r.status_code == 422


def test_get_patient(client):
    pid = client.post("/patients/", json=PATIENT).json()["id"]
    r = client.get(f"/patients/{pid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Jane Doe"


def test_get_patient_not_found(client):
    assert client.get("/patients/9999").status_code == 404


def test_list_patients_includes_created(client):
    client.post("/patients/", json=PATIENT)
    names = [p["name"] for p in client.get("/patients/").json()]
    assert names == ["John Doe", "Jane Doe"]


def test_delete_patient(client):
    pid = client.post("/patients/", json=PATIENT).json()["id"]
    r = client.delete(f"/patients/{pid}")
    assert r.status_code == 200
    assert r.json() == {"deleted": pid}
    assert client.get(f"/patients/{pid}").status_code == 404


def test_delete_patient_not_found(client):
    assert client.delete("/patients/9999").status_code == 404


def test_get_patient_invalid_id(client):
    assert client.get("/patients/abc").status_code == 422


def test_init_db_does_not_reseed(client):
    database.init_db()
    database.init_db()
    assert len(client.get("/patients/").json()) == 1


@pytest.mark.parametrize(
    "method,path,body",
    [
        ("get", "/patients/", None),
        ("get", "/patients/1", None),
        ("post", "/patients/", PATIENT),
        ("delete", "/patients/1", None),
    ],
)
def test_missing_key_rejected(anon, method, path, body):
    r = anon.request(method, path, json=body)
    assert r.status_code == 401


def test_wrong_key_rejected(anon):
    r = anon.get("/patients/", headers={"X-API-Key": "nope"})
    assert r.status_code == 401


def test_wrong_key_does_not_write(anon, client):
    anon.post("/patients/", json=PATIENT, headers={"X-API-Key": "nope"})
    assert len(client.get("/patients/").json()) == 1


def test_root_and_docs_stay_public(anon):
    assert anon.get("/").status_code == 200
    assert anon.get("/docs").status_code == 200


def test_fails_closed_when_key_not_configured(anon, monkeypatch):
    monkeypatch.delenv("API_KEY")
    r = anon.get("/patients/", headers={"X-API-Key": "anything"})
    assert r.status_code == 503
