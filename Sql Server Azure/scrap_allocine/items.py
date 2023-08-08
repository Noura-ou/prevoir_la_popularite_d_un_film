# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class AllocineBoxofficeItem(scrapy.Item):
    titre = scrapy.Field()
    boxoffice_1 = scrapy.Field()
    semaine_1 = scrapy.Field()
    boxoffice_2 = scrapy.Field()
    semaine_2 = scrapy.Field()
    
class AllocineFilmsItem(scrapy.Item):
    titre = scrapy.Field()
    date = scrapy.Field()
    réalisateur = scrapy.Field()
    titre_original = scrapy.Field()
    durée = scrapy.Field()
    type_film = scrapy.Field()
    note_presse = scrapy.Field()
    note_spectateurs = scrapy.Field()
    description = scrapy.Field()
   # genre = scrapy.Field()
    acteurs = scrapy.Field()
    annee_production = scrapy.Field()
    langue_d_origine = scrapy.Field()
    nationalités = scrapy.Field()
    nombre_article = scrapy.Field()
    budget = scrapy.Field()
    recompenses = scrapy.Field()
    distributeur = scrapy.Field()
   # box_office_total = scrapy.Field()