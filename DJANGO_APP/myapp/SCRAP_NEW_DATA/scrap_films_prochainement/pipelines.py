# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import csv
import os
from .utils import convert_to_minutes
import re 
from dotenv import load_dotenv
import os
import pypyodbc as odbc
import pyodbc
from scrapy.exceptions import DropItem

class CsvPipeline(object):
    def __init__(self, csv_file, fields_to_export):
        self.csv_file = csv_file
        self.fields_to_export = fields_to_export
        self.file = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        csv_file = settings.get('CSV_OUTPUT_FILE', 'items.csv')
        fields_to_export = settings.get('CSV_FIELDS_TO_EXPORT', [])
        return cls(csv_file, fields_to_export)

    def open_spider(self, spider):
        # Obtenir le chemin absolu du dossier parent
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Concaténer le chemin absolu du dossier parent avec le nom du dossier "dataset" et le nom du fichier CSV
        csv_file_path = os.path.join(parent_directory, 'dataset', self.csv_file)

        # Ouvrir le fichier pour écriture binaire
        self.file = open(csv_file_path, 'wb')

        # Initialiser l'exportateur CSV
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.fields_to_export)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ProcessPipeline:
    def process_item(self, item, spider):
    
        adapter = ItemAdapter(item)
        
        field_names = ['titre', 'date', 'genre', 'duree', 'realisateur', 'distributeur', 
                             'nationalites', 'langue_d_origine', 'type_film', 'annee_production', 
                              'description']
                  
        ## Strip all whitspaces from strings and handle lists
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name is not isinstance(value, list):
                # Convert the value to a string if it's not already
                adapter[field_name] = str(value).strip()
        
        ## Process the duree field
        duree_value = adapter.get('duree')
        adapter['duree'] = convert_to_minutes(duree_value)
        
        # ## Process the genre field
        genre_value = adapter.get('genre')
        if genre_value is not None and isinstance(genre_value, str):
            # Split the genres by comma and strip whitespace
            genres = [genre.strip() for genre in genre_value.split(',')]
            # Filter out genres containing '/' or digits
            genres = [genre for genre in genres if not re.search(r'[/\d]', genre)]
            # Join the genres back into a single string separated by underscores
            genres_str = "_".join(sorted(genres))
            # Remove quotes and brackets
            genres_str = re.sub(r"['\"\[\]]", "", genres_str)
            adapter['genre'] = genres_str
            # Keep only the first genre
        if genres_str:
            first_genre = genres_str.split('_')[0]
            adapter['genre'] = first_genre

        langue_d_origine_value = adapter.get('langue_d_origine')
        if langue_d_origine_value is not None and isinstance(langue_d_origine_value, str):
            # Split the languages by comma and strip whitespace
            languages = [lang.strip() for lang in langue_d_origine_value.split(',')]
            # Get the first language
            first_language = languages[0]
            adapter['langue_d_origine'] = first_language
            
        # ## Process the nombre_article field
        # nombre_article_value = adapter.get('nombre_article')
        # if nombre_article_value is not None and isinstance(nombre_article_value, str):
        #     # Use regular expression to extract the number from the text
        #     number_match = re.search(r'\d+', nombre_article_value)
        #     if number_match:
        #         # Convert the extracted number to an integer
        #         extracted_number = int(number_match.group())
        #         adapter['nombre_article'] = extracted_number
            
           
            
        return item

class AzureSQLPipeline:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_name')
        self.DB_Driver = os.getenv('DB_Driver')
        self.spider_name = None

    def open_spider(self, spider):
        self.spider_name = spider.name

        connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if self.spider_name == 'next_movies_spider':
            print("Processing item in AzureSQLPipeline:", item)
            try:
                # Vérifier si le film existe déjà dans la base de données
                existing_film_query = '''
                SELECT id FROM movies WHERE film_id_allocine = ?;
                '''
                self.cursor.execute(existing_film_query, (item['film_id_allocine'],))
                existing_film = self.cursor.fetchone()

                if existing_film:
                    print("Film déjà dans la bdd")

                    # # Mettre à jour les données du film existant
                    # pass

                else:
                    print("Film en cours d'insertion")
                    # Insérer un nouveau film
                    insert_query = '''
                    INSERT INTO movies (titre, date, duree, genre, realisateur, distributeur, nationalites, langue_d_origine, type_film, annee_production, description, film_id_allocine, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    '''
                    self.cursor.execute(insert_query, (
                        item['titre'], item['date'], item['duree'], item['genre'], item['realisateur'], item['distributeur'],
                        item['nationalites'], item['langue_d_origine'], item['type_film'],
                        item['annee_production'], item['description'], item['film_id_allocine'], item['image']
                    ))

                    self.conn.commit()
                    film_id = self.cursor.execute("SELECT @@IDENTITY").fetchone()[0]

                    # Ajouter les acteurs pour le nouveau film
                    if item['acteurs'] is None:
                        item['acteurs'] = 'Inconnu'  # Set to 'Inconnu' if actors are None
                                        # Handle None values or set default values
                    if item['duree'] is None:
                        item['duree'] = 0.0
                    
                    if item['annee_production'] is None:
                        item['annee_production'] = 0
                    
                    if item['film_id_allocine'] is None:
                        item['film_id_allocine']= 0
                    
           
                    if isinstance(item['acteurs'], str):
                        item['acteurs'] = [item['acteurs']]  # Convert single actor string to a list

                    for acteur in item['acteurs']:
                        acteur_query = '''
                        INSERT INTO actors (film_id, acteurs)
                        VALUES (?, ?);
                        '''
                        self.cursor.execute(acteur_query, (film_id, acteur))
                        self.conn.commit()

            except Exception as e:
                raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données : {e}')
            
        elif self.spider_name == 'recent_boxoffice_spider':
            try:
                # Insérer le box office pour le spider 'recent_boxoffice_spider'
                film_allocine_id = item['film_id_allocine']
                boxoffice = item['boxoffice']

                film_query = '''
                SELECT id FROM movies WHERE film_id_allocine = ?;
                '''
                self.cursor.execute(film_query, (film_allocine_id,))
                film_id_row = self.cursor.fetchone()

                if film_id_row:
                    film_id = film_id_row[0]

                    existing_boxoffice_query = '''
                    SELECT id FROM boxoffice WHERE film_allocine_id = ?;
                    '''
                    self.cursor.execute(existing_boxoffice_query, (film_allocine_id,))
                    existing_boxoffice_row = self.cursor.fetchone()

                    if existing_boxoffice_row:
                        print(f"Box office déjà existant pour le film Allociné ID {film_allocine_id}, pass.")
                    else:
                        boxoffice_insert_query = '''
                        INSERT INTO boxoffice (film_allocine_id, boxoffice, film_id)
                        VALUES (?, ?, ?);
                        '''
                        self.cursor.execute(boxoffice_insert_query, (film_allocine_id, boxoffice, film_id))
                        self.conn.commit()
                        print(f"Box office inséré pour le film Allociné ID {film_allocine_id}")
                
            except Exception as e:
                raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données : {e}')
        
        return item