import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from exceptions import InvalidOperationError, ValidationError  # noqa: E402
from models import ConsultationStatus, Doctor, Nurse, ClinicalOfficer  # noqa: E402
from repository import JsonRepository  # noqa: E402
from services import HospitalSystem  # noqa: E402


class HospitalSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.data_file = base / "data.json"
        self.rates_file = base / "rates.json"
        self.rates_file.write_text(
            json.dumps(
                {
                    "Doctor": {"standard": 50000, "review": 35000},
                    "Nurse": {"standard": 20000, "procedure": 30000},
                    "ClinicalOfficer": {"standard": 30000, "minor_procedure": 40000},
                }
            ),
            encoding="utf-8",
        )
        self.system = HospitalSystem(JsonRepository(self.data_file), self.rates_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_patient_assigns_unique_ids(self):
        p1 = self.system.register_patient("Alice A", "0700000001", 25)
        p2 = self.system.register_patient("Bob B", "0700000002", 30)
        self.assertEqual(p1.patient_id, "P0001")
        self.assertEqual(p2.patient_id, "P0002")

    def test_worker_subclasses_and_polymorphic_charges(self):
        doctor = self.system.register_health_worker("Doctor", "Dr One", "0700000011")
        nurse = self.system.register_health_worker("Nurse", "Nurse One", "0700000012")
        officer = self.system.register_health_worker("Clinical Officer", "Officer One", "0700000013")
        self.assertIsInstance(doctor, Doctor)
        self.assertIsInstance(nurse, Nurse)
        self.assertIsInstance(officer, ClinicalOfficer)
        self.assertEqual(doctor.calculate_charge("standard"), 50000)
        self.assertEqual(nurse.calculate_charge("standard"), 20000)
        self.assertEqual(officer.calculate_charge("standard"), 30000)

    def test_consultation_links_objects_and_history(self):
        patient = self.system.register_patient("Alice A", "0700000001", 25)
        worker = self.system.register_health_worker("Doctor", "Dr One", "0700000011")
        consultation = self.system.create_consultation(
            patient.patient_id, worker.worker_id, "Persistent headache", "standard", "2026-09-30"
        )
        history = self.system.patient_history(patient.patient_id)
        self.assertEqual(len(history), 1)
        self.assertIs(history[0].patient, patient)
        self.assertIs(history[0].health_worker, worker)
        self.assertEqual(consultation.charge, 50000)

    def test_complete_consultation_and_reject_double_completion(self):
        patient = self.system.register_patient("Alice A", "0700000001", 25)
        worker = self.system.register_health_worker("Nurse", "Nurse One", "0700000012")
        consultation = self.system.create_consultation(
            patient.patient_id, worker.worker_id, "Wound dressing", "procedure", "2026-09-30"
        )
        self.system.complete_consultation(consultation.consultation_id)
        self.assertEqual(consultation.status, ConsultationStatus.COMPLETED)
        with self.assertRaises(InvalidOperationError):
            self.system.complete_consultation(consultation.consultation_id)

    def test_validation_rejects_bad_inputs(self):
        with self.assertRaises(ValidationError):
            self.system.register_patient("A", "not-a-phone", -1)

        patient = self.system.register_patient("Alice A", "0700000001", 25)
        worker = self.system.register_health_worker("Doctor", "Dr One", "0700000011")
        with self.assertRaises(ValidationError):
            self.system.create_consultation(
                patient.patient_id, worker.worker_id, "Headache", "unknown_service", "2026-09-30"
            )

    def test_duplicate_phone_rejected(self):
        self.system.register_patient("Alice A", "0700000001", 25)
        with self.assertRaises(ValidationError):
            self.system.register_patient("Another Person", "0700000001", 40)

    def test_persistence_reload(self):
        patient = self.system.register_patient("Alice A", "0700000001", 25)
        worker = self.system.register_health_worker("Clinical Officer", "Officer One", "0700000013")
        consultation = self.system.create_consultation(
            patient.patient_id, worker.worker_id, "Fever and cough", "standard", "2026-09-30"
        )
        self.system.complete_consultation(consultation.consultation_id)

        reloaded = HospitalSystem(JsonRepository(self.data_file), self.rates_file)
        self.assertEqual(len(reloaded.all_patients()), 1)
        self.assertEqual(len(reloaded.all_health_workers()), 1)
        self.assertEqual(len(reloaded.consultations_by_status(ConsultationStatus.COMPLETED)), 1)
        self.assertEqual(reloaded.summary_report()["completed_revenue"], 30000)


if __name__ == "__main__":
    unittest.main()
