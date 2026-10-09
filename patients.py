import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import get_db

router = APIRouter(prefix="/patients", tags=["patients"])


class PatientIn(BaseModel):
    name: str
    age: int
    gender: str
    phone: str | None = None
    diagnosis: str | None = None


class Patient(PatientIn):
    id: int


@router.post("/", response_model=Patient, status_code=201)
def create_patient(patient: PatientIn, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        "INSERT INTO patients (name, age, gender, phone, diagnosis) VALUES (?, ?, ?, ?, ?)",
        (patient.name, patient.age, patient.gender, patient.phone, patient.diagnosis),
    )
    db.commit()
    return Patient(id=cur.lastrowid, **patient.model_dump())


@router.get("/", response_model=list[Patient])
def list_patients(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM patients").fetchall()
    return [dict(r) for r in rows]


@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return dict(row)


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"deleted": patient_id}
