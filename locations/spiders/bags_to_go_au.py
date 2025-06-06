from locations.categories import Categories, apply_category
from locations.items import Feature
from locations.storefinders.stockinstore import StockInStoreSpider


class BagsToGoAUSpider(StockInStoreSpider):
    name = "bags_to_go_au"
    item_attributes = {"brand": "Bags To Go", "brand_wikidata": "Q117745930"}
    api_site_id = "10017"
    api_widget_id = "25"
    api_widget_type = "sis"
    api_origin = "https://bagstogo.com.au"

    def parse_item(self, item: Feature, location: dict):
        apply_category(Categories.SHOP_BAG, item)
        yield item
