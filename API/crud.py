from fastapi import HTTPException
import string 
import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Utiliser les variables d'environnement chargées
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
db_driver = os.getenv("DB_DRIVER")


def clean_data(data):
    # Remplacer les valeurs manquantes par des zéros
    data = data.dropna()

    for col in data.columns:
        data[col] = data[col].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))


    # Supprimer les doublons
    data = data.drop_duplicates()

    return data


def update_actors_count_from_azure_db():
    # Connexion à la base de données Azure SQL
    conn = pyodbc.connect(f"DRIVER={db_driver};SERVER={db_server};DATABASE={db_name};UID={db_user};PWD={db_password}")
    cursor = conn.cursor()

    # Exécuter une requête SQL pour récupérer les données
    query ="""
    SELECT acteurs_films.*, COUNT(acteurs_films.acteurs_connu) as nombre_acteur_connu
    FROM acteurs_films
    INNER JOIN films ON acteurs_films.film_id = films.id
    GROUP BY acteurs_films.id, acteurs_films.film_id, acteurs_films.acteurs_connu, films.id;

    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Fermer la connexion
    conn.close()
   

    # df_azure_data = pd.read_sql(query, conn)


    # df_azure_data['nombre_acteurs_connus'] = df_azure_data['acteurs'].apply(lambda x: len([acteur for acteur in eval(x) if acteur in df_azure_data]))

    # # df_azure_data['nombre_acteurs_connus'] = df_azure_data['acteurs_connu'].apply(lambda x: x.count(',') + 1 if isinstance(x, str) else 0)

# Compter le nombre d'acteurs connus dans chaque film et créer une nouvelle colonne pour cela


    # Fermer la connexion à la base de données
    # conn.close()

    # return df_azure_data



