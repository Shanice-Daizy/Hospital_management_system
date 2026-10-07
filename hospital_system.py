"""Coordinator for the hospital outpatient management system."""

from models.clinical_officer import ClinicalOfficer
from models.consultation import Consultation
from models.doctor import Doctor
from models.nurse import Nurse
from models.patient import Patient


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
    