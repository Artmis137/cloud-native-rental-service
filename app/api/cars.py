from fastapi import APIRouter, Body, HTTPException, Query

from app.schemas.car import CarBase, Dates

# APIRouter permet de découper notre application en plusieurs fichiers
# C'est l'équivalent d'un @RestController dédié à une ressource spécifique
router = APIRouter(
    prefix="/cars",
    tags=["Cars"],
)

# Base de données simulée (en mémoire)
db_cars = [
    CarBase(plateNumber="11AA22", brand="Ferrari", price=100, is_rented=False),
    CarBase(plateNumber="AA11BB", brand="Renault", price=40, is_rented=True),
    CarBase(plateNumber="CC22DD", brand="Peugeot", price=30, is_rented=False),
]


def find_car(plateNumber: str) -> CarBase:
    """
    Cherche une voiture via sa plaque, lève une erreur 404 si elle n'existe pas.
    """
    for car in db_cars:
        if car.plateNumber == plateNumber:
            return car

    raise HTTPException(
        status_code=404,
        detail=f"Car with plate number {plateNumber} not found",
    )


@router.get("", response_model=list[CarBase])
def get_cars():
    """
    Retourne la liste des voitures non louées.
    """
    # Une liste en compréhension, considérée comme plus "pythonique"
    # que filter + lambda : list(filter(lambda car: not car.is_rented, db_cars))
    return [car for car in db_cars if not car.is_rented]


@router.get("/{plateNumber}", response_model=CarBase)
def get_car(plateNumber: str):
    """
    Retourne les détails d'une voiture spécifique via sa plaque.
    """
    return find_car(plateNumber)


@router.put("/{plateNumber}")
def update_car_status(
    # Path parameter
    plateNumber: str,
    # Query parameter
    rent: bool = Query(..., description="True pour louer, False pour restituer"),
    # Body optionnel : on n'envoie pas de dates quand on rend la voiture
    dates: Dates | None = Body(default=None),
):
    """
    Loue ou restitue une voiture spécifique via sa plaque.
    """
    car = find_car(plateNumber)

    # Si on loue la voiture, on vérifie qu'elle n'est pas déjà louée
    if rent and car.is_rented:
        raise HTTPException(
            status_code=400,
            detail=f"Car with plate number {plateNumber} is already rented",
        )
    # Si on rend la voiture, on vérifie qu'elle est bien louée
    if not rent and not car.is_rented:
        raise HTTPException(
            status_code=400,
            detail=f"Car with plate number {plateNumber} is not rented",
        )

    # On met à jour le statut de la voiture
    car.is_rented = rent

    # Si on loue la voiture avec des dates, on les affiche dans le message
    if rent and dates:
        return {
            "message": f"Car with plate number {plateNumber} has been rented from {dates.begin} to {dates.end}"
        }

    return {
        "message": f"Car with plate number {plateNumber} has been {'rented' if rent else 'returned'}"
    }
