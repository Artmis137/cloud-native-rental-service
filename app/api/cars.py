from app.shemas.car import CarBase
from fastapi import APIRouter, HTTPException
from typing import List


# APIRouter permet de découper notre application en plusieurs fichiers
# C'est l'équivalent d'un @RestController dédié à une ressource spécifique
router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)

# Base de données simulée (en mémoire)
db_cars = [
    CarBase(plateNumber="11AA22", brand="Ferrari", price=100, is_rented=False),
    CarBase(plateNumber="AA11BB", brand="Renault", price=40, is_rented=True),
    CarBase(plateNumber="CC22DD", brand="Peugeot", price=30, is_rented=False)
]

@router.get("", response_model=List[CarBase])
def get_cars() :
    """ 
    Retourne la liste des voitures non louées.
    """
    # Option 1 : ce que je prefere, avec filter et une fonction lambda 
    # return list(filter(lambda car: not car.is_rented, db_cars))
    
    # Option 2 : Avec une liste de comprehension
    # C'est souvent considéré comme plus "Pythonique" et lisible en entreprise
    return [car for car in db_cars if not car.is_rented]

@router.get("/{plateNumber}", response_model=CarBase)
def get_car(plateNumber: str) :
    """ 
    Retourne les détails d'une voiture spécifique via sa plaque
    """
    
    # On cherche la voiture dans notre fausse de base de données
    for car in db_cars:
        if car.plateNumber == plateNumber:
            return car
        
    # Si on parcourt toute la liste sans trouver, on lève erreur 404
    raise HTTPException(
        status_code=404,
        detail=f"Car with plate number {plateNumber} not found"
    )