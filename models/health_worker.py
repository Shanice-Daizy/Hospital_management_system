"""Abstract health worker model."""

from abc import abstractmethod

from models.person import Person
from validators import validate_non_empty_text, validate_positive_number


class HealthWorker(Person):
    """Define the details and behaviour shared by all health workers."""

    def __init__(
        self, worker_id, first_name, last_name, phone, department, base_fee
    ):
        super().__init__(worker_id, first_name, last_name, phone)
        self.department = department
        self.base_fee = base_fee

    

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        self._department = validate_non_empty_text(value, "Department")

    @property
    def base_fee(self):
        return self.__base_fee

    @base_fee.setter
    def base_fee(self, value):
        self.__base_fee = validate_positive_number(value, "Base fee")

    def get_role(self):
        return "Health Worker"

    @abstractmethod
    def calculate_charge(self):
        """Calculate the charge for this worker's service."""
        raise NotImplementedError

    @abstractmethod
    def provide_service(self):
        """Return the service provided by this worker."""
        raise NotImplementedError

    def __str__(self):
        return (
            f"{self.worker_id} - {self.full_name}, {self.get_role()}, "
            f"Department: {self.department}, Base fee: {self.base_fee:.2f}"
        )