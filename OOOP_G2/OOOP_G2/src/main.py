from __future__ import annotations

from pathlib import Path

from exceptions import HospitalError, ValidationError
from models import ConsultationStatus
from repository import JsonRepository
from services import HospitalSystem


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "hospital_data.json"
RATES_FILE = BASE_DIR / "config" / "service_rates.json"


def print_header(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def print_records(records, empty_message: str = "No records found.") -> None:
    records = list(records)
    if not records:
        print(empty_message)
        return
    for record in records:
        print(record)


def prompt_non_empty(label: str) -> str:
    value = input(label).strip()
    if not value:
        raise ValidationError(f"{label.rstrip(': ')} cannot be blank.")
    return value


def register_patient(system: HospitalSystem) -> None:
    print_header("REGISTER PATIENT")
    name = prompt_non_empty("Name: ")
    phone = prompt_non_empty("Phone: ")
    age = prompt_non_empty("Age: ")
    patient = system.register_patient(name, phone, age)
    print(f"Patient registered successfully. Assigned ID: {patient.patient_id}")


def register_worker(system: HospitalSystem) -> None:
    print_header("REGISTER HEALTH WORKER")
    print("Types: Doctor | Nurse | Clinical Officer")
    worker_type = prompt_non_empty("Type: ")
    name = prompt_non_empty("Name: ")
    phone = prompt_non_empty("Phone: ")
    worker = system.register_health_worker(worker_type, name, phone)
    print(f"Health worker registered successfully. Assigned ID: {worker.worker_id}")
    print(f"Available services: {', '.join(worker.available_services)}")


def create_consultation(system: HospitalSystem) -> None:
    print_header("CREATE CONSULTATION")
    patient_id = prompt_non_empty("Patient ID: ")
    worker_id = prompt_non_empty("Health worker ID: ")
    worker = system.get_health_worker(worker_id)
    print(f"Available {worker.role} services: {', '.join(worker.available_services)}")
    service_type = prompt_non_empty("Service type: ")
    complaint = prompt_non_empty("Patient complaint: ")
    entered_date = input("Consultation date YYYY-MM-DD (press Enter for today): ").strip()
    consultation = system.create_consultation(
        patient_id=patient_id,
        worker_id=worker_id,
        complaint=complaint,
        service_type=service_type,
        consultation_date=entered_date or None,
    )
    print("Consultation created successfully:")
    print(consultation)


def complete_consultation(system: HospitalSystem) -> None:
    print_header("COMPLETE CONSULTATION")
    consultation_id = prompt_non_empty("Consultation ID: ")
    consultation = system.complete_consultation(consultation_id)
    print(f"{consultation.consultation_id} marked COMPLETED.")


def cancel_consultation(system: HospitalSystem) -> None:
    print_header("CANCEL CONSULTATION")
    consultation_id = prompt_non_empty("Consultation ID: ")
    consultation = system.cancel_consultation(consultation_id)
    print(f"{consultation.consultation_id} marked CANCELLED.")


def search_patient(system: HospitalSystem) -> None:
    print_header("SEARCH PATIENTS")
    query = prompt_non_empty("Search by ID, name or phone: ")
    print_records(system.search_patients(query))


def search_worker(system: HospitalSystem) -> None:
    print_header("SEARCH HEALTH WORKERS")
    query = prompt_non_empty("Search by ID, name, phone or category: ")
    print_records(system.search_health_workers(query))


def show_patient_history(system: HospitalSystem) -> None:
    print_header("PATIENT CONSULTATION HISTORY")
    patient_id = prompt_non_empty("Patient ID: ")
    patient = system.get_patient(patient_id)
    print(f"Patient: {patient}")
    print_records(system.patient_history(patient_id), "No consultations recorded for this patient.")


def show_status(system: HospitalSystem, status: ConsultationStatus) -> None:
    print_header(f"{status.value} CONSULTATIONS")
    print_records(system.consultations_by_status(status), f"No {status.value.lower()} consultations found.")


def show_summary(system: HospitalSystem) -> None:
    print_header("SYSTEM SUMMARY REPORT")
    report = system.summary_report()
    print(f"Registered patients:       {report['patient_count']}")
    print(f"Registered health workers: {report['health_worker_count']}")
    for role, count in sorted(report["worker_counts"].items()):
        print(f"  - {role}: {count}")
    print(f"Total consultations:       {report['consultation_count']}")
    for status, count in sorted(report["status_counts"].items()):
        print(f"  - {status}: {count}")
    print(f"Completed revenue:         UGX {report['completed_revenue']:,.0f}")


def show_all_records(system: HospitalSystem) -> None:
    print_header("ALL REGISTERED PATIENTS")
    print_records(system.all_patients())
    print_header("ALL REGISTERED HEALTH WORKERS")
    print_records(system.all_health_workers())


def print_menu() -> None:
    print("""
HOSPITAL OUTPATIENT MANAGEMENT SYSTEM
1. Register patient
2. Register health worker
3. Create consultation
4. Complete consultation
5. Cancel consultation
6. Search patients
7. Search health workers
8. View patient consultation history
9. Display current consultations
10. Display completed consultations
11. Display all patients and health workers
12. View summary report
0. Exit
""")


def main() -> None:
    try:
        system = HospitalSystem(JsonRepository(DATA_FILE), RATES_FILE)
    except HospitalError as error:
        print(f"Unable to start system: {error}")
        return

    actions = {
        "1": lambda: register_patient(system),
        "2": lambda: register_worker(system),
        "3": lambda: create_consultation(system),
        "4": lambda: complete_consultation(system),
        "5": lambda: cancel_consultation(system),
        "6": lambda: search_patient(system),
        "7": lambda: search_worker(system),
        "8": lambda: show_patient_history(system),
        "9": lambda: show_status(system, ConsultationStatus.CURRENT),
        "10": lambda: show_status(system, ConsultationStatus.COMPLETED),
        "11": lambda: show_all_records(system),
        "12": lambda: show_summary(system),
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid menu option. Please choose one of the listed numbers.")
            continue
        try:
            action()
        except HospitalError as error:
            print(f"Operation rejected: {error}")
        except (ValueError, TypeError) as error:
            print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
