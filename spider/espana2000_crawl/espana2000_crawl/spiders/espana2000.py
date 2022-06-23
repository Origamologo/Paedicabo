from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner
import extruct

def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class Espana2000(CrawlSpider):
    name = 'espana2000'
    allowed_domains = ['espana2000.es']
    start_urls = ['https://espana2000.es']
    rules = (Rule(LinkExtractor()),)

    def parse_item(self, response):
        yield {
            'url': response.url,
            'metadata': extruct.extract(
                response.text,
                response.url,
                syntaxes=['opengraph', 'json-ld']
            ),
        }
# scrapy runspider espana200.py
