import json

import scrapy

from locations.hours import DAYS_FR, OpeningHours
from locations.items import Feature


class EuromasterFRSpider(scrapy.Spider):
    name = "euromaster_fr"
    start_urls = ["https://www.euromaster.fr/centres"]
    item_attributes = {"brand": "Euromaster", "brand_wikidata": "Q3060668"}

    def parse(self, response):
        regions = response.xpath('//*[@class="list-province w-100"]//@href').getall()
        for region in regions:
            yield scrapy.Request(url=region, callback=self.parse_region)

    def parse_region(self, response):
        cities = response.xpath('//*[@class="list-province w-100"]//@href').getall()
        for city in cities:
            yield scrapy.Request(url=city, callback=self.parse_city)

    def parse_city(self, response):
        shops = set(response.xpath("//a[text()='Voir la fiche centre']/@href").getall())
        for shop in shops:
            yield scrapy.Request(url=shop, callback=self.parse_shop)

    def parse_shop(self, response):
        data = json.loads(response.xpath('//*[@type="application/ld+json"]/text()').get())
        if not data["name"].startswith("Euromaster"):
            return
        item = Feature()
        item["ref"] = item["website"] = response.url
        item["name"] = data["name"]
        item["phone"] = data["telephone"]
        item["street_address"] = data["address"]["streetAddress"]
        item["postcode"] = data["address"]["postalCode"]
        item["city"] = data["address"]["addressLocality"]
        item["lat"] = data["geo"]["latitude"]
        item["lon"] = data["geo"]["longitude"]
        item["opening_hours"] = self.parse_opening_hours(response)
        yield item

    def parse_opening_hours(self, response):
        oh = OpeningHours()
        days = response.xpath('//*[@class="tableHoraires"]/tr/th/text()').getall()
        hours = response.xpath('//*[@class="tableHoraires"]/tr/td/text()').getall()
        for day, hour in zip(days, hours):
            oh.add_ranges_from_string(ranges_string=day + " " + hour, days=DAYS_FR, delimiters=[" - "])

        return oh.as_opening_hours()
