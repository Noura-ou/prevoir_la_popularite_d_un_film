from fastapi import HTTPException
import string 
import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd
import ast 
import re

# Charger les variables d'environnement à partir du fichier .env


# def clean_data(data):
#     # Remplacer les valeurs manquantes par des zéros
#     data = data.dropna()

#     for col in data.columns:
#         data[col] = data[col].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))


#     # Supprimer les doublons
#     data = data.drop_duplicates()

#     return data


# def update_actors_count_from_azure_db():
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

    # Exécuter une requête SQL pour récupérer les données
    # query ="""
    # SELECT acteurs_films.*, COUNT(acteurs_films.acteurs_connu) as nombre_acteur_connu
    # FROM acteurs_films
    # INNER JOIN films ON acteurs_films.film_id = films.id
    # GROUP BY acteurs_films.id, acteurs_films.film_id, acteurs_films.acteurs_connu, films.id;

    # """
df_acteurs_connus = pd.read_csv('API/top_acteurs.csv')

acteurs_connus = set(df_acteurs_connus['acteur'])


query= """ SELECT titre,duree, distributeur,realisateur,nationalites, langue_d_origine,
       type_film, annee_production, acteurs_films.acteurs
            FROM films
            INNER JOIN acteurs_films ON films.id = acteurs_films.film_id;
    """

    # cursor.execute(query)
    # results = cursor.fetchall()

   

df_azure_data = pd.read_sql(query, conn)


df_azure_data['nombre_acteurs_connus'] = df_azure_data['acteurs'].apply(lambda x: len([acteur for acteur in eval(x) if acteur in acteurs_connus]))
# df_azure_data['nombre_acteurs_connus'] = df_azure_data['acteurs'].apply(lambda x: len([acteur for acteur in eval(x) if acteur in df_acteurs_connus]))

#df_azure_data['nombre_acteurs_connus'] = acteurs_connus.apply(lambda x: x.count(',') + 1 if isinstance(x, str) else 0)

# Utiliser ast.literal_eval() pour convertir les chaînes de caractères en listes d'acteurs

# Utiliser la fonction extract_actors pour extraire les noms d'acteurs de la colonne acteurs



    
   
conn.close()
#return df_azure_data
print(df_azure_data)




  


 
