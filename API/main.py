from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import numpy as np
import pandas as pd
import re
import crud 
import pyodbc



# server = 'your_server.database.windows.net'
# database = 'your_database'
# username = 'your_username'
# password = 'your_password'
# driver= '{ODBC Driver 17 for SQL Server}'

model = joblib.load('modele.pkl')

app = FastAPI()

class FilmInput(BaseModel):
    annee_production: float
    durée: float
    nombre_article: float


# @app.get("/update_actors_count/")
# def update_actors_count():
#     df_actors_data = crud.update_actors_count_from_azure_db()
#     return df_actors_data.to_dict(orient='records')
     
@app.post("/predict/")
def predict_film_boxoffice(film: FilmInput):

    data = crud.update_actors_count_from_azure_db()

    df_actors_data = pd.DataFrame(data, columns=['titre'])


    prediction_data = [[film.annee_production, film.durée, film.nombre_article]]

    # Créer un DataFrame pandas à partir des données de prédiction
    df_prediction = pd.DataFrame(prediction_data, columns=["annee_production", "durée", "nombre_article"])

    # Nettoyer les données en appelant la fonction clean_data depuis le module crud.py
    df_prediction = crud.clean_data(df_prediction)

    # Utiliser le modèle chargé pour effectuer des prédictions
    prediction = model.predict(df_prediction)

    return {"box_office_prediction": prediction[0]}
