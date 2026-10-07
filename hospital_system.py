"""Coordinator for the hospital outpatient management system."""

from models.clinical_officer import ClinicalOfficer
from models.consultation import Consultation
from models.doctor import Doctor
from models.nurse import Nurse
from models.patient import Patient
from validators import validate_non_empty_text

class HospitalSystem:
    """Coordinates patients, health workers and consultations."""

    def __init__(self):
        self.__patients = {}
        self.__health_workers = {}
        self.__consultations = {}

        self.__next_patient_number = 1
        self.__next_worker_number = 1
        self.__next_consultation_number = 1

    def __generate_patient_id(self):
        patient_id = f"P{self.__next_patient_number:04d}"
        self.__next_patient_number += 1
        return patient_id

    def __generate_worker_id(self):
        worker_id = f"HW{self.__next_worker_number:04d}"
        self.__next_worker_number += 1
        return worker_id

    def __generate_consultation_id(self):
        consultation_id = f"C{self.__next_consultation_number:04d}"
        self.__next_consultation_number += 1
        return consultation_id
    def register_patient(
        self, first_name, last_name, phone, date_of_birth, address
    ):
        patient_id = self.__generate_patient_id()

        try:
            patient = Patient(
                patient_id,
                first_name,
                last_name,
                phone,
                date_of_birth,
                address,
            )
        except ValueError:
            self.__next_patient_number -= 1
            raise

        self.__patients[patient_id] = patient
        return patient

    def find_patient(self, patient_id):
        key = str(patient_id).strip().upper()

        patient = self.__patients.get(key)

        if patient is None:
            raise ValueError(f"Patient '{key}' was not found.")

        return patient

    def list_patients(self):
        return list(self.__patients.values())
    def register_health_worker(
        self,
        worker_type,
        first_name,
        last_name,
        phone,
        department,
        base_fee,
        specialty=None,
    ):
        cleaned_type = validate_non_empty_text(
            worker_type, "Health worker type"
        ).lower().replace("_", " ").replace("-", " ")

        worker_classes = {
            "doctor": Doctor,
            "nurse": Nurse,
            "clinical officer": ClinicalOfficer,
            "clinicalofficer": ClinicalOfficer,
        }

        worker_class = worker_classes.get(cleaned_type)

        if worker_class is None:
            raise ValueError(
                "Worker type must be Doctor, Nurse, or Clinical Officer."
            )

        worker_id = self.__generate_worker_id()

        try:
            common_details = (
                worker_id,
                first_name,
                last_name,
                phone,
                department,
                base_fee,
            )

            if worker_class is Doctor:
                worker = Doctor(*common_details, specialty)
            else:
                worker = worker_class(*common_details)

        except ValueError:
            self.__next_worker_number -= 1
            raise

        self.__health_workers[worker_id] = worker
        return worker

    def find_health_worker(self, worker_id):
        key = str(worker_id).strip().upper()

        worker = self.__health_workers.get(key)

        if worker is None:
            raise ValueError(f"Health worker '{key}' was not found.")

        return worker

    def list_health_workers(self):
        return list(self.__health_workers.values())
        def search_patients(self, query):
        search_text = str(query).strip().lower()
        matches = []

        for patient in self.__patients.values():
            searchable_values = (
                patient.patient_id,
                patient.first_name,
                patient.last_name,
                patient.full_name,
                patient.phone,
            )

            if any(
                search_text in str(value).lower()
                for value in searchable_values
            ):
                matches.append(patient)

        return matches

    def search_health_workers(self, query):
        search_text = str(query).strip().lower()
        matches = []

        for worker in self.__health_workers.values():
            searchable_values = [
                worker.worker_id,
                worker.first_name,
                worker.last_name,
                worker.full_name,
                worker.phone,
                worker.department,
                worker.get_role(),
            ]

            if isinstance(worker, Doctor):
                searchable_values.append(worker.specialty)

            if any(
                search_text in str(value).lower()
                for value in searchable_values
            ):
                matches.append(worker)

        return matches