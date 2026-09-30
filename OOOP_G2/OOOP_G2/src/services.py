from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Type

from exceptions import RecordNotFoundError, ValidationError
from models import (
    ClinicalOfficer,
    Consultation,
    ConsultationStatus,
    Doctor,
    HealthWorker,
    Nurse,
    Patient,
)
from repository import JsonRepository


class HospitalSystem:
    """Coordinates domain objects while keeping menu/UI logic separate."""

    WORKER_CLASSES: Dict[str, Type[HealthWorker]] = {
        "doctor": Doctor,
        "nurse": Nurse,
        "clinicalofficer": ClinicalOfficer,
        "clinical officer": ClinicalOfficer,
    }

    def __init__(self, repository: JsonRepository, rates_file: str | Path):
        self._repository = repository
        self._rates = self._load_rates(rates_file)
        self._patients: Dict[str, Patient] = {}
        self._workers: Dict[str, HealthWorker] = {}
        self._consultations: Dict[str, Consultation] = {}
        self._load_records()

    @staticmethod
    def _load_rates(rates_file: str | Path) -> dict:
        path = Path(rates_file)
        try:
            with path.open("r", encoding="utf-8") as file:
                rates = json.load(file)
        except FileNotFoundError as exc:
            raise ValidationError(f"Service rate configuration not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise ValidationError("Service rate configuration contains invalid JSON.") from exc

        for category in ("Doctor", "Nurse", "ClinicalOfficer"):
            if category not in rates or not isinstance(rates[category], dict) or not rates[category]:
                raise ValidationError(f"Missing or empty rate configuration for {category}.")
        return rates

    def _load_records(self) -> None:
        data = self._repository.load()

        for item in data["patients"]:
            patient = Patient(**item)
            self._patients[patient.patient_id] = patient

        for item in data["health_workers"]:
            worker_type = str(item.get("worker_type", ""))
            cls = self.WORKER_CLASSES.get(worker_type.lower())
            if cls is None:
                raise ValidationError(f"Unknown health worker type stored in data: {worker_type}")
            worker = cls(
                worker_id=item["worker_id"],
                name=item["name"],
                phone=item["phone"],
                service_rates=self._rates[cls.role],
            )
            self._workers[worker.worker_id] = worker

        for item in data["consultations"]:
            patient = self._patients.get(item["patient_id"])
            worker = self._workers.get(item["worker_id"])
            if patient is None or worker is None:
                raise ValidationError(
                    f"Consultation {item.get('consultation_id', '<unknown>')} references a missing patient or health worker."
                )
            consultation = Consultation(
                consultation_id=item["consultation_id"],
                patient=patient,
                health_worker=worker,
                consultation_date=item["consultation_date"],
                complaint=item["complaint"],
                service_type=item["service_type"],
                status=item["status"],
                charge=item["charge"],
            )
            self._consultations[consultation.consultation_id] = consultation

    def _persist(self) -> None:
        self._repository.save(
            {
                "patients": [patient.to_dict() for patient in self._patients.values()],
                "health_workers": [worker.to_dict() for worker in self._workers.values()],
                "consultations": [consultation.to_dict() for consultation in self._consultations.values()],
            }
        )

    @staticmethod
    def _ensure_unique_phone(phone: str, records: Iterable, label: str) -> None:
        normalized = str(phone).strip().replace(" ", "")
        if any(getattr(record, "phone", None) == normalized for record in records):
            raise ValidationError(f"A {label} with phone number {normalized} is already registered.")

    def register_patient(self, name: str, phone: str, age: int) -> Patient:
        self._ensure_unique_phone(phone, self._patients.values(), "patient")
        patient_id = self._repository.next_id(self._patients.keys(), "P")
        patient = Patient(patient_id, name, phone, age)
        self._patients[patient.patient_id] = patient
        self._persist()
        return patient

    def register_health_worker(self, worker_type: str, name: str, phone: str) -> HealthWorker:
        key = " ".join(str(worker_type).strip().lower().split())
        cls = self.WORKER_CLASSES.get(key)
        if cls is None:
            raise ValidationError("Health worker type must be Doctor, Nurse, or Clinical Officer.")
        self._ensure_unique_phone(phone, self._workers.values(), "health worker")
        worker_id = self._repository.next_id(self._workers.keys(), "HW")
        worker = cls(worker_id, name, phone, self._rates[cls.role])
        self._workers[worker.worker_id] = worker
        self._persist()
        return worker

    def get_patient(self, patient_id: str) -> Patient:
        key = str(patient_id).strip().upper()
        if key not in self._patients:
            raise RecordNotFoundError(f"Patient '{patient_id}' was not found.")
        return self._patients[key]

    def get_health_worker(self, worker_id: str) -> HealthWorker:
        key = str(worker_id).strip().upper()
        if key not in self._workers:
            raise RecordNotFoundError(f"Health worker '{worker_id}' was not found.")
        return self._workers[key]

    def get_consultation(self, consultation_id: str) -> Consultation:
        key = str(consultation_id).strip().upper()
        if key not in self._consultations:
            raise RecordNotFoundError(f"Consultation '{consultation_id}' was not found.")
        return self._consultations[key]

    def create_consultation(
        self,
        patient_id: str,
        worker_id: str,
        complaint: str,
        service_type: str,
        consultation_date: str | None = None,
    ) -> Consultation:
        patient = self.get_patient(patient_id)
        worker = self.get_health_worker(worker_id)
        worker.provide_service(service_type)  # polymorphic call + service validation
        consultation_id = self._repository.next_id(self._consultations.keys(), "C")
        consultation = Consultation(
            consultation_id=consultation_id,
            patient=patient,
            health_worker=worker,
            consultation_date=consultation_date or date.today().isoformat(),
            complaint=complaint,
            service_type=service_type,
        )
        self._consultations[consultation.consultation_id] = consultation
        self._persist()
        return consultation

    def complete_consultation(self, consultation_id: str) -> Consultation:
        consultation = self.get_consultation(consultation_id)
        consultation.complete()
        self._persist()
        return consultation

    def cancel_consultation(self, consultation_id: str) -> Consultation:
        consultation = self.get_consultation(consultation_id)
        consultation.cancel()
        self._persist()
        return consultation

    def search_patients(self, query: str) -> List[Patient]:
        q = str(query).strip()
        if not q:
            raise ValidationError("Search query cannot be blank.")
        return [patient for patient in self._patients.values() if patient.matches(q)]

    def search_health_workers(self, query: str) -> List[HealthWorker]:
        q = str(query).strip()
        if not q:
            raise ValidationError("Search query cannot be blank.")
        return [worker for worker in self._workers.values() if worker.matches(q)]

    def patient_history(self, patient_id: str) -> List[Consultation]:
        patient = self.get_patient(patient_id)
        return sorted(
            [c for c in self._consultations.values() if c.patient.patient_id == patient.patient_id],
            key=lambda item: (item.consultation_date, item.consultation_id),
            reverse=True,
        )

    def consultations_by_status(self, status: ConsultationStatus | str) -> List[Consultation]:
        target = status if isinstance(status, ConsultationStatus) else ConsultationStatus(str(status).upper())
        return sorted(
            [c for c in self._consultations.values() if c.status == target],
            key=lambda item: (item.consultation_date, item.consultation_id),
        )

    def all_patients(self) -> List[Patient]:
        return list(self._patients.values())

    def all_health_workers(self) -> List[HealthWorker]:
        return list(self._workers.values())

    def summary_report(self) -> dict:
        status_counts = Counter(c.status.value for c in self._consultations.values())
        worker_counts = Counter(worker.role for worker in self._workers.values())
        completed_revenue = sum(
            c.charge for c in self._consultations.values() if c.status == ConsultationStatus.COMPLETED
        )
        return {
            "patient_count": len(self._patients),
            "health_worker_count": len(self._workers),
            "worker_counts": dict(worker_counts),
            "consultation_count": len(self._consultations),
            "status_counts": dict(status_counts),
            "completed_revenue": completed_revenue,
        }
