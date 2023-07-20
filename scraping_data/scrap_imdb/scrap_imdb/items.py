# Define here the models for your scraped items
import scrapy



class ScrapImdbItem(scrapy.Item):
    titre = scrapy.Field()
    date = scrapy.Field()
    réalisateur = scrapy.Field()
    titre_original = scrapy.Field()
    durée = scrapy.Field()
    type_film = scrapy.Field()
    # score = scrapy.Field()
    # nbr_votants = scrapy.Field()
    desciption = scrapy.Field()
    genre = scrapy.Field()
    acteurs = scrapy.Field()
    box_office_fr = scrapy.Field()
    langue_d_origine = scrapy.Field()
    nationnalités = scrapy.Field()
    # Sociétés_de_production = scrapy.Field()
