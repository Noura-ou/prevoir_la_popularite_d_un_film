import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AllocineBoxofficeItem
from scrapy.settings import Settings

# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'CSV_OUTPUT_FILE': 'boxoffice_tous.csv',
    'CSV_FIELDS_TO_EXPORT': ['titre','semaine_1', 'boxoffice_1', 'boxoffice_2'  ],  
    'MONGODB_COLLECTION': 'boxoffice_tous',
    }

class BoxofficeSpider(CrawlSpider):
    name = "boxoffice_spider"
    custom_settings = CUSTOM_SETTINGS
    
    allowed_domains = ["allocine.fr"]
    
    DEPTH_LIMIT = 5

    # URL de la première page
    base_url = 'https://www.allocine.fr/films'
    num_pages = 100

    def start_requests(self):
        # Générer les URL de pagination
        for page in range(1, self.num_pages + 1):
            url = f"{self.base_url}/?page={page}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Récupérer les titres de films sur la page actuelle
        titres = response.css("a.meta-title-link::text").getall()

        # Récupérer les liens des films sur la page actuelle
        film_links = response.css("a.meta-title-link::attr(href)").getall()

        # Combinaison des titres et des liens des films
        for titre, film_link in zip(titres, film_links):
            # Suivre le lien du film pour accéder à la page du film
            yield response.follow(film_link, callback=self.parse_film, meta={'titre': titre.strip()})

    def parse_film(self, response):
        # Extraire le titre du film à partir des informations stockées dans la méta
        titre = response.meta['titre']
        # Extraire le numéro du film à partir de l'URL
        film_id = response.url.split("cfilm=")[-1].split(".html")[0]
        # Construire l'URL du box office
        box_office_url = f"https://www.allocine.fr/film/fichefilm-{film_id}/box-office/"
        # Suivre le lien du box office pour accéder à la page du box office
        yield scrapy.Request(box_office_url, callback=self.parse_box_office, meta={'titre': titre})

    def parse_box_office(self, response):
        # Extract the box office fr of the first week
        # box_office = response.css("td[data-heading='Entrées']::text").get()

        semaine_selector = response.css("td[data-heading='Semaine']")
        semaines = semaine_selector.css("::text").getall()
        semaine_1 = semaines[1]

        # Extract the first two lines of the "Entrées" column
        entrees_selector = response.css("td[data-heading='Entrées']")
        boxoffice_1 = entrees_selector[0].css("::text").get().strip()
        boxoffice_2 = entrees_selector[1].css("::text").get().strip()

        allocine_movies_items = AllocineBoxofficeItem()
        allocine_movies_items['titre'] = response.meta['titre']
        allocine_movies_items['semaine_1'] = semaine_1
        allocine_movies_items['boxoffice_1'] = boxoffice_1
        allocine_movies_items['boxoffice_2'] = boxoffice_2

        yield allocine_movies_items
    

