from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
from typing import Dict, List

from exceptions import InvalidOperationError, ValidationError


class ConsultationStatus(str, Enum):
    CURRENT = "CURRENT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Patient:
    """Represents an outpatient registered at the hospital."""

    def __init__(self, patient_id: str, name: str, phone: str, age: int, registered_on: str | None = None):
        self.__patient_id = self._validate_id(patient_id, "P")  # private
        self._name = ""  # protected by convention
        self._phone = ""
        self.name = name
        self.phone = phone
        self.age = age
        self.registered_on = registered_on or date.today().isoformat()  # public

    @staticmethod
    def _validate_id(value: str, prefix: str) -> str:
        value = str(value).strip().upper()
        if not value.startswith(prefix) or not value[len(prefix):].isdigit():
            raise ValidationError(f"ID must use the format {prefix} followed by digits.")
        return value

    @property
    def patient_id(self) -> str:
        return self.__patient_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        cleaned = " ".join(str(value).split())
        if len(cleaned) < 2:
            raise ValidationError("Patient name must contain at least 2 characters.")
        if not any(char.isalpha() for char in cleaned):
            raise ValidationError("Patient name must contain letters.")
        self._name = cleaned

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        cleaned = str(value).strip().replace(" ", "")
        if cleaned.startswith("+"):
            digits = cleaned[1:]
        else:
            digits = cleaned
        if not digits.isdigit() or not (7 <= len(digits) <= 15):
            raise ValidationError("Phone number must contain 7 to 15 digits, optionally starting with '+'.")
        self._phone = cleaned

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        try:
            numeric = int(value)
        except (TypeError, ValueError) as exc:
            raise ValidationError("Age must be a whole number.") from exc
        if not (0 <= numeric <= 130):
            raise ValidationError("Age must be between 0 and 130.")
        self._age = numeric

    def matches(self, query: str) -> bool:
        q = str(query).strip().lower()
        return q in self.patient_id.lower() or q in self.name.lower() or q in self.phone.lower()

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "phone": self.phone,
            "age": self.age,
            "registered_on": self.registered_on,
        }

    def __str__(self) -> str:
        return f"{self.patient_id} | {self.name} | Age {self.age} | {self.phone}"


class HealthWorker(ABC):
    """Abstract superclass for all categories of health workers."""

    role = "HealthWorker"  # public class attribute

    def __init__(self, worker_id: str, name: str, phone: str, service_rates: Dict[str, float]):
        self.__worker_id = Patient._validate_id(worker_id, "HW")  # private
        self._name = ""  # protected
        self._phone = ""
        self._service_rates = self._validate_rates(service_rates)  # protected
        self.name = name
        self.phone = phone

    @staticmethod
    def _validate_rates(service_rates: Dict[str, float]) -> Dict[str, float]:
        if not isinstance(service_rates, dict) or not service_rates:
            raise ValidationError("Each health worker category requires at least one configured service rate.")
        cleaned: Dict[str, float] = {}
        for service, amount in service_rates.items():
            key = str(service).strip().lower()
            if not key:
                raise ValidationError("Service names cannot be blank.")
            try:
                numeric = float(amount)
            except (TypeError, ValueError) as exc:
                raise ValidationError(f"Invalid charge configured for service '{service}'.") from exc
            if numeric < 0:
                raise ValidationError("Service charges cannot be negative.")
            cleaned[key] = numeric
        return cleaned

    @property
    def worker_id(self) -> str:
        return self.__worker_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        cleaned = " ".join(str(value).split())
        if len(cleaned) < 2 or not any(char.isalpha() for char in cleaned):
            raise ValidationError("Health worker name must contain at least 2 characters and include letters.")
        self._name = cleaned

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        cleaned = str(value).strip().replace(" ", "")
        digits = cleaned[1:] if cleaned.startswith("+") else cleaned
        if not digits.isdigit() or not (7 <= len(digits) <= 15):
            raise ValidationError("Phone number must contain 7 to 15 digits, optionally starting with '+'.")
        self._phone = cleaned

    @property
    def available_services(self) -> List[str]:
        return list(self._service_rates.keys())

    def matches(self, query: str) -> bool:
        q = str(query).strip().lower()
        return (
            q in self.worker_id.lower()
            or q in self.name.lower()
            or q in self.phone.lower()
            or q in self.role.lower()
        )

    def _rate_for(self, service_type: str) -> float:
        service_key = str(service_type).strip().lower()
        if service_key not in self._service_rates:
            options = ", ".join(self.available_services)
            raise ValidationError(f"'{service_type}' is not available for {self.role}. Choose: {options}.")
        return self._service_rates[service_key]

    @abstractmethod
    def provide_service(self, service_type: str) -> str:
        """Describe how this category of health worker provides a service."""

    @abstractmethod
    def calculate_charge(self, service_type: str) -> float:
        """Return the charge for a service; subclasses must implement this polymorphically."""

    def to_dict(self) -> dict:
        return {
            "worker_id": self.worker_id,
            "name": self.name,
            "phone": self.phone,
            "worker_type": self.role,
        }

    def __str__(self) -> str:
        services = ", ".join(self.available_services)
        return f"{self.worker_id} | {self.name} | {self.role} | {self.phone} | Services: {services}"


class Doctor(HealthWorker):
    role = "Doctor"

    def provide_service(self, service_type: str) -> str:
        self._rate_for(service_type)
        return f"Doctor consultation/service: {service_type.strip().lower()}"

    def calculate_charge(self, service_type: str) -> float:
        return self._rate_for(service_type)


class Nurse(HealthWorker):
    role = "Nurse"

    def provide_service(self, service_type: str) -> str:
        self._rate_for(service_type)
        return f"Nursing outpatient service: {service_type.strip().lower()}"

    def calculate_charge(self, service_type: str) -> float:
        return self._rate_for(service_type)


class ClinicalOfficer(HealthWorker):
    role = "ClinicalOfficer"

    def provide_service(self, service_type: str) -> str:
        self._rate_for(service_type)
        return f"Clinical officer service: {service_type.strip().lower()}"

    def calculate_charge(self, service_type: str) -> float:
        return self._rate_for(service_type)


class Consultation:
    """Associates one Patient with one HealthWorker for an outpatient encounter."""

    def __init__(
        self,
        consultation_id: str,
        patient: Patient,
        health_worker: HealthWorker,
        consultation_date: str,
        complaint: str,
        service_type: str,
        status: ConsultationStatus | str = ConsultationStatus.CURRENT,
        charge: float | None = None,
    ):
        self.__consultation_id = Patient._validate_id(consultation_id, "C")
        self.patient = patient  # association
        self.health_worker = health_worker  # association
        self.consultation_date = consultation_date
        self.complaint = complaint
        self.service_type = service_type
        self.status = status
        calculated = health_worker.calculate_charge(self.service_type) if charge is None else float(charge)
        if calculated < 0:
            raise ValidationError("Consultation charge cannot be negative.")
        self.__charge = calculated

    @property
    def consultation_id(self) -> str:
        return self.__consultation_id

    @property
    def consultation_date(self) -> str:
        return self._consultation_date

    @consultation_date.setter
    def consultation_date(self, value: str) -> None:
        cleaned = str(value).strip()
        try:
            parsed = datetime.strptime(cleaned, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValidationError("Consultation date must use YYYY-MM-DD format.") from exc
        self._consultation_date = parsed.isoformat()

    @property
    def complaint(self) -> str:
        return self._complaint

    @complaint.setter
    def complaint(self, value: str) -> None:
        cleaned = " ".join(str(value).split())
        if len(cleaned) < 3:
            raise ValidationError("Complaint must contain at least 3 characters.")
        self._complaint = cleaned

    @property
    def service_type(self) -> str:
        return self._service_type

    @service_type.setter
    def service_type(self, value: str) -> None:
        cleaned = str(value).strip().lower()
        if not cleaned:
            raise ValidationError("Service type cannot be blank.")
        self._service_type = cleaned

    @property
    def status(self) -> ConsultationStatus:
        return self._status

    @status.setter
    def status(self, value: ConsultationStatus | str) -> None:
        try:
            self._status = value if isinstance(value, ConsultationStatus) else ConsultationStatus(str(value).upper())
        except ValueError as exc:
            valid = ", ".join(status.value for status in ConsultationStatus)
            raise ValidationError(f"Invalid consultation status. Use one of: {valid}.") from exc

    @property
    def charge(self) -> float:
        return self.__charge

    def complete(self) -> None:
        if self.status == ConsultationStatus.COMPLETED:
            raise InvalidOperationError("This consultation is already completed.")
        if self.status == ConsultationStatus.CANCELLED:
            raise InvalidOperationError("A cancelled consultation cannot be completed.")
        self.status = ConsultationStatus.COMPLETED

    def cancel(self) -> None:
        if self.status == ConsultationStatus.COMPLETED:
            raise InvalidOperationError("A completed consultation cannot be cancelled.")
        self.status = ConsultationStatus.CANCELLED

    def to_dict(self) -> dict:
        return {
            "consultation_id": self.consultation_id,
            "patient_id": self.patient.patient_id,
            "worker_id": self.health_worker.worker_id,
            "consultation_date": self.consultation_date,
            "complaint": self.complaint,
            "service_type": self.service_type,
            "status": self.status.value,
            "charge": self.charge,
        }

    def __str__(self) -> str:
        return (
            f"{self.consultation_id} | {self.consultation_date} | "
            f"Patient: {self.patient.name} ({self.patient.patient_id}) | "
            f"Worker: {self.health_worker.name} ({self.health_worker.role}) | "
            f"Service: {self.service_type} | Status: {self.status.value} | "
            f"Charge: UGX {self.charge:,.0f} | Complaint: {self.complaint}"
        )
