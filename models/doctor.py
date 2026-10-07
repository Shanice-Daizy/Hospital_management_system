"""The Doctor model."""

from models.health_worker import HealthWorker
from validators import validate_non_empty_text


class Doctor(HealthWorker):
    """Represent a doctor who provides medical consultations."""

    CHARGE_MULTIPLIER = 1.50
    SERVICE_NAME = "Medical Consultation"

    def __init__(
        self,
        worker_id,
        first_name,
        last_name,
        phone,
        department,
        base_fee,
        specialty,
    ):
        super().__init__(
            worker_id, first_name, last_name, phone, department, base_fee
        )
        self.specialty = specialty

    

    @specialty.setter
    def specialty(self, value):
        self.__specialty = validate_non_empty_text(value, "Specialty")

    def calculate_charge(self):
        return self.base_fee * self.CHARGE_MULTIPLIER

    def provide_service(self):
        return self.SERVICE_NAME

    def get_role(self):
        return "Doctor"

    def __str__(self):
        return f"{super().__str__()}, Specialty: {self.specialty}"
