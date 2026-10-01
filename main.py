"""Terminal interface for the Hospital Outpatient Management System."""

from hospital_system import HospitalSystem
from validators import validate_consultation_date, validate_date_of_birth


MENU = """
==================================================
 HOSPITAL OUTPATIENT MANAGEMENT SYSTEM
==================================================

PATIENT MANAGEMENT
1. Register Patient
2. List Patients
3. Search Patients

HEALTH WORKER MANAGEMENT
4. Register Health Worker
5. List Health Workers
6. Search Health Workers

CONSULTATION MANAGEMENT
7. Create Consultation
8. Start Consultation
9. Complete Consultation
10. Cancel Consultation

HISTORY & REPORTS
11. View Patient Consultation History
12. View Health Worker Consultation History
13. View Scheduled Consultations
14. View Current Consultations
15. View Completed Consultations
16. View Cancelled Consultations
17. View All Consultations
18. View System Summary

0. Exit
"""


def display_records(records, empty_message="No records found."):
    """Print each record in a collection."""
    if not records:
        print(empty_message)
        return
    for record in records:
        print(record)


def register_patient(system):
    print("\nREGISTER PATIENT")
    patient = system.register_patient(
        input("First name: "),
        input("Last name: "),
        input("Phone: "),
        validate_date_of_birth(input("Date of birth (YYYY-MM-DD): ")),
        input("Address: "),
    )
    print(f"Patient registered successfully: {patient}")
