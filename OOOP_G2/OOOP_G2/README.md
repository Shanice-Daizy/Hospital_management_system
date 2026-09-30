# OOOP_G2 — Hospital Outpatient Management System

This folder contains the completed Group 2 Object-Oriented Programming assignment.

## What is included

- `src/` — modular Python source code.
- `config/service_rates.json` — editable consultation/service charges (kept outside the Python source so rates are not hard-coded).
- `data/hospital_data.json` — persistent application data. It starts empty; records are created through the program.
- `uml/` — UML class diagram in PNG and DOT source form.
- `report/` — short Word report explaining the design and all required OOP concepts.
- `tests/` — automated tests used to cross-check the implementation.
- `demo/` — a practical demonstration guide for class presentation.

## Requirements

- Python 3.10 or later.
- No external Python packages are required to run the application.

## Run the application

From the `OOOP_G2` folder:

```bash
python src/main.py
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Important design note

The assignment does not specify exact consultation charges. Therefore, example rates are stored in `config/service_rates.json` rather than being embedded in the Python classes. They can be changed without editing source code.

## Demonstration checklist

1. Register a patient and show the generated patient ID.
2. Register at least a Doctor, Nurse, and Clinical Officer.
3. Create consultations using different health-worker categories and show different service charges.
4. Search for patients and workers.
5. View a patient's consultation history.
6. Complete one consultation and compare current vs completed consultation lists.
7. Attempt an invalid operation, such as an unsupported service, invalid phone number, or completing the same consultation twice.
8. Show the summary report.
9. Point to the code sections for encapsulation, relationships, inheritance, polymorphism, and abstraction.
