from fastapi import HTTPException
import string 
import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd
import ast 
import unicodedata
import re

def update_from_azure_db():
    load_dotenv()
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_name')
    DB_Driver = os.getenv('DB_Driver')



# Établissez la connexion à votre base de données
    connection_string = f'Driver={DB_Driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = """ SELECT titre,
                   MAX(duree) AS duree,
                   MAX(distributeur) AS distributeur,
                   MAX(realisateur) AS realisateur,
                   MAX(nationalites) AS nationalites,
                   MAX(langue_d_origine) AS langue_d_origine,
                   MAX(type_film) AS type_film,
                   MAX(genre) AS genre,
                   MAX(annee_production) AS annee_production,
                   STRING_AGG(acteurs, ',') AS acteurs,
                   STRING_AGG(top_acteurs.acteur, ',') AS acteur
                   FROM films
                   INNER JOIN acteurs_films ON films.id = acteurs_films.film_id
                   INNER JOIN top_acteurs ON acteurs_films.id_acteurs_films = top_acteurs.id
                   GROUP BY titre;
        """

        df_azure_data = pd.read_sql(query, conn)

        # Fermer la connexion après utilisation
        conn.close()

        # Fonction pour nettoyer le nom d'un acteur
        def clean_name(name):
            name = name.lower()  # Convertir en minuscules
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')  # Supprimer les accents
            name = name.replace(" ", "")  # Supprimer les espaces
            return name

        # Calculer le nombre d'acteurs connus
        def calculate_known_actors(row):
            actor = clean_name(row['acteur'][0])
            actors = [clean_name(a) for a in row['acteurs']]

            return sum(actor in a for a in actors)

        def calculate_known_realisateur(row):
            actor = clean_name(row['acteur'][0])
            realisateur = [clean_name(a) for a in row['realisateur']]

            return int(any(actor in a for a in realisateur))

        df_azure_data['nombre_acteurs_connus'] = df_azure_data.apply(calculate_known_actors, axis=1)
        df_azure_data['realisateur_connu'] = df_azure_data.apply(calculate_known_realisateur, axis=1)

        unique_genres = set(g for row in df_azure_data['genre'] for g in row)

        for genre in unique_genres:
            df_azure_data[genre] = df_azure_data['genre'].apply(lambda x: 1 if genre in x else 0)

        return df_azure_data

    except pyodbc.Error as err:
        raise HTTPException(status_code=500, detail="Error connecting to the Azure database")
#return df_azure_data
#print(df_azure_data.columns)



  


 
