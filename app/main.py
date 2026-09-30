from fastapi import FastAPI

# On crée l'insrtance de notre applicaiton (équivalent du contexte Spring Boot)
# C'est une bonne pratique de renseigner le title et la decription pour la documentation générée
app = FastAPI(
    title="Car Rental API",
    description="TP Cloud Native - Service de location de voitures",
    version="1.0.0"
) 

# Equivalent de @RestC