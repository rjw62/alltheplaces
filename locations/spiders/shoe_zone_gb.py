from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider


class ShoeZoneGBSpider(SitemapSpider, StructuredDataSpider):
    name = "shoe_zone_gb"
    item_attributes = {
        "brand": "Shoe Zone",
        "brand_wikidata": "Q7500016",
        "country": "GB",
    }
    sitemap_urls = ["https://www.shoezone.com/sitemap_stores.xml"]
    sitemap_rules = [(r"https:\/\/www\.shoezone\.com\/Stores\/[-._\w]+-(\d+)$", "parse_sd")]
    wanted_types = ["ShoeStore"]

    def post_process_item(self, item, response, ld_data, **kwargs):
        # lat/lon are both parsed into lat, separate them
        (item["lat"], item["lon"]) = item["lat"]
        yield item
