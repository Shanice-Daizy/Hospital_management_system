"""Tests for registering and reporting nurses in the hospital system."""

import unittest

from hospital_system import HospitalSystem
from models.nurse import Nurse


class NurseRegistrationTests(unittest.TestCase):
    def test_registration_makes_nurse_available_to_system_queries(self):
        system = HospitalSystem()

        nurse = system.register_health_worker(
            "Nurse", "Alex", "Kim", "555-0101", "Outpatient", 85
        )

        self.assertIsInstance(nurse, Nurse)
        self.assertEqual(nurse.worker_id, "HW001")
        self.assertIs(system.find_health_worker("hw001"), nurse)
        self.assertEqual(system.list_health_workers(), [nurse])
        self.assertEqual(system.search_health_workers("nurse"), [nurse])
        self.assertEqual(system.get_summary()["nurses"], 1)
        self.assertEqual(system.get_summary()["health_workers"], 1)


if __name__ == "__main__":
    unittest.main()
