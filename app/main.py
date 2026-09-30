from app.api import cars
from fastapi import FastAPI

# On crée l'insrtance de notre applicaiton (équivalent du contexte Spring Boot)
# C'est une bonne pratique de renseigner le title et la decription pour la documentation générée
app = FastAPI(
    title="Car Rental API",
    description="TP Cloud Native - Service de location de voitures",
    version="1.0.0"
) 

app.include_router(cars.router) # on attache les routes des voitures à l'API principale

# Equivalent de @RestController et @GetMapping("/")
@app.get("/")
def hello() -> str:
    """_summary_

    Health check endpoint basique.
    """
    return "Hello world!"