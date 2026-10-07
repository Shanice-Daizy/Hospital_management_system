
"""Domain models for the hospital outpatient system."""

from models.clinical_officer import ClinicalOfficer
from models.consultation import Consultation
from models.doctor import Doctor
from models.health_worker import HealthWorker
from models.nurse import Nurse
from models.patient import Patient
from models.person import Person

__all__ = [
    "Person",
    "Patient",
    "HealthWorker",
    "Doctor",
    "Nurse",
    "ClinicalOfficer",
    "Consultation",
]
