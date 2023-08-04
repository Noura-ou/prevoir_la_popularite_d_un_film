
# @app.post("/predict/")
# def predict_film_boxoffice(film: FilmInput):
#     try:
# data = crud.update_from_azure_db()


# df_azure = pd.DataFrame(data, columns=['titre'])
# print(df_azure)

#         # Créer un DataFrame pandas à partir des données de prédiction
#         df_prediction = pd.DataFrame(df_azure, columns=["film"])

#         # Utiliser le modèle chargé pour effectuer des prédictions
#         prediction = model.predict(df_prediction)

#         return {"box_office_prediction": prediction[0]}
    
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error in predicting film box office")



# @app.post("/predict/")
# def predict_film_boxoffice(film: FilmInput):
#     try:

# from fastapi import FastAPI, HTTPException
# import joblib
# from pydantic import BaseModel
# import pandas as pd
# import crud

# model = joblib.load('pipeml.joblib')


# class FilmInput(BaseModel):
#     titre: str

# data = crud.update_from_azure_db()

# # Instancier un objet de la classe FilmInput pour obtenir le titre du film
# film_input = FilmInput(titre="The First Slam Dunk")  # Remplacez "Titre du film" par le titre du film réel que vous souhaitez utiliser

# # Récupérez le titre du film à partir de l'objet FilmInput
# film_titre = film_input.titre

# # Filtrer les données pour garder uniquement les informations concernant le film spécifié
# film_data = data[data['titre'] == film_titre]

# # cols_to_drop = ['titre', 'acteurs', 'acteurs_connus', 'réalisateur','genres']
# # X_azure = film_data.drop(cols_to_drop, axis=1)
# prediction = model.predict(film_data)
# print(prediction)

#         X_azure = film_data.drop(cols_to_drop, axis=1)
# #         if film_data.empty:
#             raise HTTPException(status_code=404, detail="Film non trouvé dans la base de données")

#         # Supprimez la colonne 'titre' car elle a été supprimée pendant l'entraînement
#         X_azure = film_data.drop(['titre'], axis=1)

#         # Utilisez le modèle chargé et le pipeline de prétraitement pour la prédiction
#         prediction = pipeline.predict(X_azure)

#         return {"box_office_prediction": prediction[0]}
    
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Erreur lors de la prédiction du box-office du film")
from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
import pandas as pd
import crud

# Charger le modèle pré-entraîné
model = joblib.load('pipeml.joblib')

app = FastAPI()

class FilmInput(BaseModel):
    titre: str

@app.post("/predict/")
def predict_film_boxoffice(film: FilmInput):
    try:
        data = crud.update_from_azure_db()

        # Récupérer le titre du film à partir de l'objet FilmInput
        film_titre = film.titre

        # Filtrer les données pour garder uniquement les informations concernant le film spécifié
        film_data = data[data['titre'] == film_titre]

        if film_data.empty:
            raise HTTPException(status_code=404, detail="Film non trouvé dans la base de données")

        # Faire les prédictions avec le modèle chargé
        prediction = model.predict(film_data)

        return {"box_office_prediction": int(prediction)}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la prédiction du box-office du film")

