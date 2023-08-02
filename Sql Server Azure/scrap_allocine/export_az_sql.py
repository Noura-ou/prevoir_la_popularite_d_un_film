import csv
import pyodbc
from dotenv import load_dotenv
import os




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

def delete_table(table_name):
        drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
        cursor.execute(drop_table_query)
        conn.commit()

        # Delete les table s'il existent
delete_table('top_acteurs')
    
    
# Obtenir le chemin absolu du répertoire actuel
current_directory = os.path.dirname(os.path.abspath(__file__))
# Spécifier le nom du fichier CSV
csv_file_name = 'top_acteurs.csv'

# Concaténer le chemin absolu avec le nom du fichier CSV
csv_file_path = os.path.join(current_directory, csv_file_name)


create_table_query = '''
        CREATE TABLE top_acteurs (
            id INT IDENTITY(1,1) PRIMARY KEY,
            acteur VARCHAR(500),
        );
        '''

# Exécutez la requête pour créer la table
cursor.execute(create_table_query)
conn.commit()


# Spécifiez le nom de la table dans la base de données où vous souhaitez importer les données
table_name = 'top_acteurs'

# Définissez le nom des colonnes dans le fichier CSV dans le même ordre que dans la table
columns = ['acteur' ]  # Remplacez par les noms de vos colonnes

# Ouvrez le fichier CSV et insérez les données dans la base de données
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        values = [row[column] for column in columns]
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
        cursor.execute(query, values)
        conn.commit()

# Fermez la connexion
conn.close()
