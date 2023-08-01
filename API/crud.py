from fastapi import HTTPException
import string 
import pyodbc



server = 'your_server.database.windows.net'
database = 'your_database'
username = 'your_username'
password = 'your_password'
driver= '{ODBC Driver 17 for SQL Server}'


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
    conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")

    # Exécuter une requête SQL pour récupérer les données
    query = "SELECT * FROM films_table;"
    df_azure_data = pd.read_sql(query, conn)

    # Mettre à jour la colonne 'nombre_acteurs_connus' avec le nombre d'acteurs connus à partir de la colonne 'acteurs_connu'
    df_azure_data['nombre_acteurs_connus'] = df_azure_data['acteurs_connu'].apply(lambda x: x.count(',') + 1 if isinstance(x, str) else 0)

    # Fermer la connexion à la base de données
    conn.close()

    return df_azure_data



