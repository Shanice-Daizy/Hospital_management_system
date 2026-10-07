"""Tests for the nurse consultation workflow."""

import unittest
from datetime import date

from hospital_system import HospitalSystem


class NurseConsultationWorkflowTests(unittest.TestCase):
    def test_nurse_consultation_lifecycle_updates_history_and_billing(self):
        system = HospitalSystem()
        patient = system.register_patient(
            "Taylor", "Morgan", "555-0100", "1990-01-01", "Main St"
        )
        nurse = system.register_health_worker(
            "Nurse", "Alex", "Kim", "555-0101", "Outpatient", 85
        )

        consultation = system.create_consultation(
            patient.patient_id,
            nurse.worker_id,
            date.today().isoformat(),
            "Routine assessment",
        )

        self.assertEqual(consultation.service, "Nursing Assessment")
        self.assertEqual(consultation.charge, 85)
        self.assertEqual(system.get_scheduled_consultations(), [consultation])

        system.start_consultation(consultation.consultation_id)
        self.assertEqual(system.get_current_consultations(), [consultation])

        system.complete_consultation(
            consultation.consultation_id, "Assessment complete"
        )

        self.assertEqual(
            system.get_health_worker_history(nurse.worker_id), [consultation]
        )
        self.assertEqual(system.get_patient_history(patient.patient_id), [consultation])
        self.assertEqual(system.get_completed_consultations(), [consultation])
        self.assertEqual(system.get_summary()["completed_charges"], 85)


if __name__ == "__main__":
    unittest.main()
