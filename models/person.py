"""Abstract base class for people in the outpatient system."""

from abc import ABC, abstractmethod

from validators import validate_name, validate_non_empty_text, validate_phone


class Person(ABC):
    """Store common personal details and define a common role interface."""

    def __init__(self, person_id, first_name, last_name, phone):
        self.__id = validate_non_empty_text(person_id, "ID")
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = validate_name(value, "First name")

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = validate_name(value, "Last name")

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = validate_phone(value)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def get_role(self):
        """Return the person's role in the system."""
        raise NotImplementedError

    def __str__(self):
        return f"{self.id} - {self.full_name} ({self.get_role()})"
class man 