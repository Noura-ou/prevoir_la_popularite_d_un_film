<<<<<<< HEAD


=======
>>>>>>> c3309edc3b9047f88228db40ffe78147e37ac234
from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
import pandas as pd
from . import crud
import os




# Obtiens le chemin absolu du répertoire du script en cours
script_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin vers le modèle pré-entraîné dans le même répertoire
model_path = os.path.join(script_dir, 'pipem.joblib')

# Charger le modèle pré-entraîné
<<<<<<< HEAD
model = joblib.load('best_model.joblib')       
=======
model = joblib.load(model_path)
>>>>>>> c3309edc3b9047f88228db40ffe78147e37ac234

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


<<<<<<< HEAD
=======

@app.post("/predict/")
def predict_film_boxoffice(film: FilmInput):
    try:
        data = crud.update_from_azure_db()
>>>>>>> c3309edc3b9047f88228db40ffe78147e37ac234


# @app.post("/predict/")
# def predict_film_boxoffice(film: FilmInput):
#     try:
#         data = crud.update_from_azure_db()

#         # Récupérer le titre du film à partir de l'objet FilmInput
#         film_titre = film.titre

#         # Filtrer les données pour garder uniquement les informations concernant le film spécifié
#         film_data = data[data['titre'].str.lower() == film_titre.lower()]

#         print("Données filtrées :", film_data)

<<<<<<< HEAD
#         if film_data.empty:
#             raise HTTPException(status_code=404, detail="Film non trouvé dans la base de données")

#         # Faire les prédictions avec le modèle chargé
#         prediction = model.predict(film_data)

#         return {"box_office_prediction": int(abs(prediction))}
    
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Erreur lors de la prédiction du box-office du film")



=======
        return {"box_office_prediction": int(abs(prediction))}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la prédiction du box-office du film")
>>>>>>> c3309edc3b9047f88228db40ffe78147e37ac234
