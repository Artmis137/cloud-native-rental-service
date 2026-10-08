from app.shemas.car import CarBase, Dates
from fastapi import APIRouter, HTTPException,  Query, Body
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
    
@router.put("/{plateNumber}")
def update_car_status(
    # Path parameter    
    plateNumber: str,
    
    # Query parameter 
    rent: bool =  Query(..., description="True pour louer, Fasle      pour  restituer"),
    
    # Body
    # Il est optionnel    (Dates | None) car       on n'envoie pas dedates quand on rend la voiture
    dates: Dates | None = Body(default=None)
) :
    """ 
    Loue ou restitue une voiture spécifique via sa plaque
    """
    
    # On cherche la voiture dans notre fausse de base de données
    for car in db_cars:
        if car.plateNumber == plateNumber:
            # Si on loue la voiture, on vérifie qu'elle n'est pas déjà louée
            if rent and car.is_rented:
                raise HTTPException(
                    status_code=400,
                    detail=f"Car with plate number {plateNumber} is already rented"
                )
            # Si on rend la voiture, on vérifie qu'elle est bien louée
            if not rent and not car.is_rented:
                raise HTTPException(
                    status_code=400,
                    detail=f"Car with plate number {plateNumber} is not rented"
                )
            
            # On met à jour le statut de la voiture
            car.is_rented = rent
            
            # Si on loue la voiture, on affiche les dates de location
            if rent and dates:
                return {
                    "message": f"Car with plate number {plateNumber} has been rented from {dates.begin} to {dates.end}"
                }
            
            return {
                "message": f"Car with plate number {plateNumber} has been {'rented' if rent else 'returned'}"
            }
        
    # Si on parcourt toute la liste sans trouver, on lève erreur 404
    raise HTTPException(
        status_code=404,
        detail=f"Car with plate number {plateNumber} not found"
    )
    