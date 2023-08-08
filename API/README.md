
# Documentation de l'API de Prédiction de Box Office de Films


## Description

Ce projet consiste en une API basée sur FastAPI qui permet de prédire le box office d'un film en fonction de ses caractéristiques. L'API utilise un modèle pré-entraîné pour effectuer ces prédictions.

## Installation

1. Cloner ce dépôt sur votre machine locale.
2. Assurez-vous que vous avez toutes les dépendances requises installées. Vous pouvez les installer en exécutant `pip install -r requirements.txt` dans le répertoire du projet.
3. Assurez-vous d'avoir placé le fichier du modèle pré-entraîné (`pipem.joblib`) dans le même répertoire que les fichiers de l'API.
4. creer un fichier .env dans le dossier API en notant les infos de connexion a la bdd azure suivants :
DB_USER='sqladmincinema'
DB_PASSWORD='Simplon@123456789'
DB_SERVER='rg-ousfia.database.windows.net'
DB_name='BDD_Cinéma_ IA'
DB_Driver='ODBC Driver 18 for SQL Server'
5.executer ces commandes une part une pour linstallation des dependences des fichiers driver_odbc et install_dependies: -sudo apt-get update,
sudo apt-get install unixodbc-dev, chmod +x Driver_ODBC_Azure.sh
,./Driver_ODBC_Azure.sh,chmod +x install_dependencies.sh,./install_dependencies.sh





## Utilisation

1. Exécutez l'API en exécutant le fichier `main.py` à l'aide de la commande `uvicorn main:app --reload`.
2. Accédez à l'URL [http://localhost:8000/docs](http://localhost:8000/docs) dans votre navigateur pour accéder à l'interface Swagger de l'API. Vous pouvez utiliser cette interface pour tester les points d'extrémité de l'API.
3. Utilisez le point d'extrémité `/predict/` pour prédire le box office d'un film en fournissant le titre du film en tant que paramètre.

## Fonctionnement

Le code se compose de deux principaux fichiers : `crud.py` et `main.py`.

### `crud.py`

Ce fichier contient une fonction `update_from_azure_db()` qui effectue les opérations suivantes :

1. Établir une connexion à une base de données Azure SQL à l'aide de la bibliothèque `pyodbc`.
2. Exécuter une requête SQL pour récupérer les données des films, notamment le titre, la durée, le distributeur, le réalisateur, les nationalités, la langue d'origine, le type de film, les genres, l'année de production, les acteurs et les acteurs connus.
3. Nettoyer et transformer les données en remplaçant les valeurs manquantes par des valeurs spécifiques (0 pour 'durée' et 'annee_production', 'inconnu' pour les autres colonnes).
4. Effectuer des opérations de nettoyage supplémentaires, telles que le nettoyage des noms d'acteurs, le calcul du nombre d'acteurs connus et la création de colonnes pour chaque genre de film.
5. Renvoyer un DataFrame avec les données nettoyées et préparées.
















# Prévoir la popularité d'un film
Développer un modèle de machine learning afin d'aider un gérant de salle de cinéma à optimiser sa programmation.
# Contexte du projet


Un gérant de salle de cinéma souhaite développer un outil d'aide à la décision pour définir les films à projeter dans sa salle de cinéma.  Actuellement, il définit la programmation en se tenant au courant des dernières nouveautés, en assistant à des festivals (Cannes, Deauville, etc.). C'est un travail très chronophage. L'outil, qui doit prédire les films qui généreront le plus d'entrées en première semaine, vise à optimiser la programmation et maximiser les revenus. Le cinéma en question dispose de quatre salles avec les capacités suivantes :

    salle 1 : 140 personnes
    salle 2 : 100 personnes
    salle 3 : 80 personnes
    salle 4 : 80 personnes

​

Le gérant estime qu'il peut capter environ 1/3000 des spectateurs nationaux. L'objectif principal est de maximiser les revenus, tandis que la diversification des genres et des styles de films est une considération secondaire.



## Features
 ⚠️ - In progress


## Run the project Locally

Clone the project

```bash
git clone https://github.com/Noura-ou/prevoir_la_popularite_d_un_film.git
````

Go to the project directory :

```bash
  cd my-project
```


## Useful Documentation

- [Requests Library in Python - Beginner Crash Course](https://www.youtube.com/watch?v=Xi1F2ZMAZ7Q)
- [Site API](https://openweathermap.org/api/hourly-forecast#name5)
- [FastAPI](https://fastapi.tiangolo.com/) 
- [Python](https://docs.python.org/3/)


## Authors

- [@noura-ou](https://github.com/Noura-ou)
- [@RolaMmss](https://github.com/RolaMmss)
- [@MyriamLbhn](https://github.com/MyriamLbhn)
- [@namineelbb ](https://github.com/amineelbb)

