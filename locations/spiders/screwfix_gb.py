from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from locations.linked_data_parser import LinkedDataParser

import html
import json

class ScrewfixGBSpider(CrawlSpider):
    name = "screwfix_gb"
    item_attributes = {"brand": "Screwfix", "brand_wikidata": "Q7439115"}
    allowed_domains = ["www.screwfix.com"]
    download_delay = 1
    start_urls = ["https://www.screwfix.com/stores/all"]
    rules = [Rule(LinkExtractor(allow=r"\/stores\/([A-Z][A-Z][0-9])\/.+$"), callback="parse")]
    wanted_types = ["HardwareStore"]

    def parse(self, response):
        data = response.xpath('//script[@type="application/ld+json"][contains(., "HardwareStore")]/text()').get()
        if data:
            data = html.unescape(data)
            data_json = json.loads(data)
            if data_json:
                item = LinkedDataParser.parse_ld(data_json)
                item['website'] = response.url
                yield item
