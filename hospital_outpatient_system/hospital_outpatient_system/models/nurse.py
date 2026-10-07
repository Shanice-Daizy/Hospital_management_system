"""Nurse model."""

from models.health_worker import HealthWorker


class Nurse(HealthWorker):
    """Represent a nurse who provides a nursing assessment."""

    CHARGE_MULTIPLIER = 1.00
    SERVICE_NAME = "Nursing Assessment"

    def calculate_charge(self):
        return self.base_fee * self.CHARGE_MULTIPLIER

    def provide_service(self):
        return self.SERVICE_NAME

    def get_role(self):
        return "Nurse"

    def __str__(self):
        return super().__str__()
