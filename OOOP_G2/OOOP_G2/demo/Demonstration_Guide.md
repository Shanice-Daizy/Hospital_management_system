# Group 2 Practical Demonstration Guide

Use this as a speaking/order guide. The values below are demonstration examples only; the program itself starts with no patient or consultation records.

## 1. Introduce the system

“Our project is a Hospital Outpatient Management System. It registers patients and health workers, creates consultations, calculates service charges, tracks consultation status, supports searches and history, and generates a summary report.”

## 2. Register sample records

Suggested examples:
- Patient: Amina Kato, 0700123456, age 24.
- Doctor: Dr Peter Okello, 0701000001.
- Nurse: Sarah Namusoke, 0701000002.
- Clinical Officer: James Ouma, 0701000003.

Point out that IDs are generated automatically (for example `P0001` and `HW0001`) rather than typed by the user.

## 3. Demonstrate inheritance and abstraction

Open `src/models.py` and show:
- `HealthWorker(ABC)` is abstract.
- `provide_service()` and `calculate_charge()` are abstract methods.
- `Doctor`, `Nurse`, and `ClinicalOfficer` inherit from `HealthWorker` and override those methods.

## 4. Demonstrate polymorphism

Create consultations with different worker categories. The same `calculate_charge(service_type)` call is sent to different subclass objects, and each object resolves the charge from the services configured for its category.

## 5. Demonstrate encapsulation

Show:
- Private identifiers such as `__patient_id`, `__worker_id`, and `__consultation_id`.
- Protected attributes such as `_name` and `_service_rates`.
- `@property` setters that validate names, phones, age, complaint, date, service type and status.

## 6. Demonstrate relationships

Explain that a `Consultation` object associates exactly one `Patient` with exactly one `HealthWorker`. `HospitalSystem` manages collections of these collaborating objects and uses `JsonRepository` for persistence.

## 7. Show required transactions

- Search for a patient.
- Search for a health worker.
- Display the patient's consultation history.
- Show current consultations.
- Complete one consultation.
- Show completed consultations.
- Show the summary report.

## 8. Show a rejected operation

Try one of these:
- Register a patient with an invalid phone number.
- Create a Doctor consultation using an unsupported service name.
- Complete a consultation twice.

Explain that the system rejects the operation with a clear message rather than failing silently.
