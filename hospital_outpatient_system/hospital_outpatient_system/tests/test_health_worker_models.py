"""Tests for health-worker roles and consultation billing."""

import unittest

from models.clinical_officer import ClinicalOfficer
from models.consultation import Consultation
from models.doctor import Doctor
from models.nurse import Nurse
from models.patient import Patient


class HealthWorkerModelTests(unittest.TestCase):
    def setUp(self):
        self.patient = Patient(
            "P-001", "Taylor", "Morgan", "555-0100", "1990-01-01", "Main St"
        )

    def test_worker_roles_provide_their_services_and_charges(self):
        workers = (
            (
                Nurse("N-001", "Alex", "Kim", "555-0101", "Nursing", 100),
                "Nurse",
                "Nursing Assessment",
                100,
            ),
            (
                ClinicalOfficer(
                    "C-001", "Sam", "Lee", "555-0102", "Outpatient", 100
                ),
                "Clinical Officer",
                "Clinical Consultation",
                120,
            ),
            (
                Doctor(
                    "D-001",
                    "Jamie",
                    "Patel",
                    "555-0103",
                    "Outpatient",
                    100,
                    "Family Medicine",
                ),
                "Doctor",
                "Medical Consultation",
                150,
            ),
        )

        for worker, role, service, charge in workers:
            with self.subTest(role=role):
                self.assertEqual(worker.get_role(), role)
                self.assertEqual(worker.provide_service(), service)
                self.assertEqual(worker.calculate_charge(), charge)

    def test_consultation_uses_workers_service_and_calculated_charge(self):
        workers = (
            (
                Nurse("N-001", "Alex", "Kim", "555-0101", "Nursing", 100),
                "Nursing Assessment",
                100,
            ),
            (
                ClinicalOfficer(
                    "C-001", "Sam", "Lee", "555-0102", "Outpatient", 100
                ),
                "Clinical Consultation",
                120,
            ),
            (
                Doctor(
                    "D-001",
                    "Jamie",
                    "Patel",
                    "555-0103",
                    "Outpatient",
                    100,
                    "Family Medicine",
                ),
                "Medical Consultation",
                150,
            ),
        )

        for worker, service, charge in workers:
            with self.subTest(role=worker.get_role()):
                consultation = Consultation(
                    "CNS-001",
                    self.patient,
                    worker,
                    "2026-10-07",
                    "Routine assessment",
                )
                self.assertEqual(consultation.service, service)
                self.assertEqual(consultation.charge, charge)


if __name__ == "__main__":
    unittest.main()
