from django.db import models

class Film(models.Model):
    titre = models.CharField(max_length=100)
    date_de_sortie = models.DateField()
    duree = models.IntegerField()  # Durée en minutes
    genre = models.CharField(max_length=50)
    nombre_entrees_estimees = models.IntegerField(default=0)  # Champ pour stocker l'estimation du nombre d'entrées en première semaine
    # champs à ajouter
    
    def __str__(self):
        return self.titre