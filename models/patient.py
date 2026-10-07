"""Patient model."""

from datetime import date

from models.person import Person
from validators import validate_date_of_birth, validate_non_empty_text


class Patient(Person):
    """Represent a registered outpatient."""

    def __init__(
        self, patient_id, first_name, last_name, phone, date_of_birth, address
    ):
        super().__init__(patient_id, first_name, last_name, phone)
        self.date_of_birth = date_of_birth
        self.address = address

    @property
    def patient_id(self):
        return self.id

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self.__date_of_birth = validate_date_of_birth(value)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = validate_non_empty_text(value, "Address")

    @property
    def age(self):
        today = date.today()
        birthday_has_passed = (today.month, today.day) >= (
            self.date_of_birth.month,
            self.date_of_birth.day,
        )
        return today.year - self.date_of_birth.year - (not birthday_has_passed)

    def get_role(self):
        return "Patient"

    def __str__(self):
        return (
            f"{self.patient_id} - {self.full_name}, Age: {self.age}, "
            f"Phone: {self.phone}, Address: {self.address}"
        )
    