from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
import pandas as pd
import crud

model = joblib.load('modele.pkl')
app = FastAPI()

class FilmInput(BaseModel):
    titre: str

@app.post("/predict/")
def predict_film_boxoffice(film: FilmInput):
    try:
        data = crud.update_from_azure_db()
        df_azure = pd.DataFrame(data, columns=['titre'])

        # Créer un DataFrame pandas à partir des données de prédiction
        df_prediction = pd.DataFrame(df_azure, columns=["titre"])

        # Utiliser le modèle chargé pour effectuer des prédictions
        prediction = model.predict(df_prediction)

        return {"box_office_prediction": prediction[0]}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in predicting film box office")
