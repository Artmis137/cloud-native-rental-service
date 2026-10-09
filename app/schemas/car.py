from datetime import date

from pydantic import BaseModel, model_validator


class CarBase(BaseModel):
    """
    Représente une voiture du parc de location.

    Attributes:
        plateNumber (str): Numéro d'immatriculation (identifiant unique).
        brand (str): Marque de la voiture.
        price (float): Prix de la location par jour.
        is_rented (bool): Indique si la voiture est actuellement louée.
    """
    plateNumber: str
    brand: str
    price: float
    is_rented: bool = False


class Dates(BaseModel):
    """
    Période de location.

    Attributes:
        begin (date): Date de début de la location (format AAAA-MM-JJ).
        end (date): Date de fin de la location (format AAAA-MM-JJ).
    """
    begin: date
    end: date

    @model_validator(mode="after")
    def check_period(self) -> "Dates":
        # La date de fin ne peut pas précéder la date de début
        if self.end < self.begin:
            raise ValueError("end date must be after or equal to begin date")
        return self
