from django.db import models
from django.utils import timezone




class Film(models.Model):
    titre = models.CharField(max_length=500)
    distributeur = models.CharField(max_length=500)
    # date = models.DateField(default=timezone.now)
    type_film = models.CharField(max_length=100, default='Unknown')  # Add a default value here


    class Meta:
        db_table = 'dataset_model_ML'



class Acteurs_films(models.Model):
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    acteurs = models.CharField(max_length=500)

    class Meta:
        db_table = 'actors'


class Movies(models.Model):
    titre = models.CharField(max_length=500)
    image = models.URLField(max_length=200)  # Champ pour stocker l'URL de l'image
    date = models.DateField(default=timezone.now)
    class Meta:
        db_table = 'movies'
