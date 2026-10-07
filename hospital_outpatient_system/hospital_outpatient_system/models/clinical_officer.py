"""Clinical officer model."""

from models.health_worker import HealthWorker


class ClinicalOfficer(HealthWorker):
    """Represent a clinical officer."""

    CHARGE_MULTIPLIER = 1.20
    SERVICE_NAME = "Clinical Consultation"

    def calculate_charge(self):
        return self.base_fee * self.CHARGE_MULTIPLIER

    def provide_service(self):
        return self.SERVICE_NAME

    def get_role(self):
        return "Clinical Officer"

    def __str__(self):
        return super().__str__()
