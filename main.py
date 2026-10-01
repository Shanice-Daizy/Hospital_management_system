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


def register_health_worker(system):
    print("\nREGISTER HEALTH WORKER")
    worker_type = input("Type (Doctor/Nurse/Clinical Officer): ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone: ")
    department = input("Department: ")
    base_fee = input("Base fee: ")
    specialty = None
    if worker_type.strip().lower() == "doctor":
        specialty = input("Specialty: ")
    worker = system.register_health_worker(
        worker_type,
        first_name,
        last_name,
        phone,
        department,
        base_fee,
        specialty,
    )
    print(f"Health worker registered successfully: {worker}")


def create_consultation(system):
    print("\nCREATE CONSULTATION")
    consultation = system.create_consultation(
        input("Patient ID: "),
        input("Health worker ID: "),
        validate_consultation_date(
            input("Consultation date (YYYY-MM-DD): ")
        ),
        input("Complaint: "),
    )
    print(f"Consultation created successfully: {consultation}")


def start_consultation(system):
    consultation = system.start_consultation(input("Consultation ID: "))
    print(f"Consultation {consultation.consultation_id} is now CURRENT.")


def complete_consultation(system):
    consultation_id = input("Consultation ID: ")
    notes = input("Completion notes: ")
    consultation = system.complete_consultation(consultation_id, notes)
    print(f"Consultation {consultation.consultation_id} was completed.")


def cancel_consultation(system):
    consultation_id = input("Consultation ID: ")
    reason = input("Cancellation reason: ")
    consultation = system.cancel_consultation(consultation_id, reason)
    print(f"Consultation {consultation.consultation_id} was cancelled.")


def display_summary(system):
    summary = system.get_summary()
    print("\nSYSTEM SUMMARY")
    print(f"Patients: {summary['patients']}")
    print(f"Total health workers: {summary['health_workers']}")
    print(f"Doctors: {summary['doctors']}")
    print(f"Nurses: {summary['nurses']}")
    print(f"Clinical officers: {summary['clinical_officers']}")
    print(f"Total consultations: {summary['consultations']}")
    print(f"Scheduled: {summary['scheduled']}")
    print(f"Current: {summary['current']}")
    print(f"Completed: {summary['completed']}")
    print(f"Cancelled: {summary['cancelled']}")
    print(f"Completed consultation charges: {summary['completed_charges']:.2f}")


def handle_menu_choice(system, choice):
    """Call the operation selected by the user."""
    if choice == "1":
        register_patient(system)
    elif choice == "2":
        display_records(system.list_patients(), "No patients registered.")
    elif choice == "3":
        display_records(system.search_patients(input("Search text: ")))
    elif choice == "4":
        register_health_worker(system)
    elif choice == "5":
        display_records(
            system.list_health_workers(), "No health workers registered."
        )
    elif choice == "6":
        display_records(system.search_health_workers(input("Search text: ")))
    elif choice == "7":
        create_consultation(system)
    elif choice == "8":
        start_consultation(system)
    elif choice == "9":
        complete_consultation(system)
    elif choice == "10":
        cancel_consultation(system)
    elif choice == "11":
        display_records(
            system.get_patient_history(input("Patient ID: ")),
            "This patient has no consultations.",
        )
    elif choice == "12":
        display_records(
            system.get_health_worker_history(input("Health worker ID: ")),
            "This health worker has no consultations.",
        )
    elif choice == "13":
        display_records(system.get_scheduled_consultations())
    elif choice == "14":
        display_records(system.get_current_consultations())
    elif choice == "15":
        display_records(system.get_completed_consultations())
    elif choice == "16":
        display_records(system.get_cancelled_consultations())
    elif choice == "17":
        display_records(system.get_all_consultations())
    elif choice == "18":
        display_summary(system)
    else:
        print("Invalid menu choice. Please enter a number from 0 to 18.")
