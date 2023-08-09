

from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
import pandas as pd
import crud

# Charger le modèle pré-entraîné
model = joblib.load('best_model.joblib')       

app = FastAPI()

class FilmInput(BaseModel):
    titre: str

data = crud.update_from_azure_db()

# Création d'une instance de FilmInput avec le titre du film souhaité
film = FilmInput(titre="Une nuit")

# Récupération du titre du film à partir de l'objet FilmInput
film_titre = film.titre

# Filtrer les données pour garder uniquement les informations concernant le film spécifié
film_data = data[data['titre'].str.lower() == film_titre.lower()]

print(film_data.columns)

prediction = model.predict(film_data)

print(prediction)




# @app.post("/predict/")
# def predict_film_boxoffice(film: FilmInput):
#     try:
#         data = crud.update_from_azure_db()

#         # Récupérer le titre du film à partir de l'objet FilmInput
#         film_titre = film.titre

#         # Filtrer les données pour garder uniquement les informations concernant le film spécifié
#         film_data = data[data['titre'].str.lower() == film_titre.lower()]

#         print("Données filtrées :", film_data)

#         if film_data.empty:
#             raise HTTPException(status_code=404, detail="Film non trouvé dans la base de données")

#         # Faire les prédictions avec le modèle chargé
#         prediction = model.predict(film_data)

#         return {"box_office_prediction": int(abs(prediction))}
    
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Erreur lors de la prédiction du box-office du film")



