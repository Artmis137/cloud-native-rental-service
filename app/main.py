from fastapi import FastAPI

from app.api import cars

# On crée l'instance de notre application (équivalent du contexte Spring Boot)
# C'est une bonne pratique de renseigner le titre et la description pour la documentation générée
app = FastAPI(
    title="Car Rental API",
    description="TP Cloud Native - Service de location de voitures",
    version="1.0.0",
)

# On attache les routes des voitures à l'API principale
app.include_router(cars.router)


# Équivalent de @RestController et @GetMapping("/")
@app.get("/")
def hello() -> str:
    """
    Health check endpoint basique.
    """
    return "Hello world!"
