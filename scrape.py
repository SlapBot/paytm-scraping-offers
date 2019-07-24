import requests
from time import sleep
from dateutil.parser import parse
from lxml import html


class Scrape(object):
    def __init__(self):
        self.all_categories = []

    @staticmethod
    def get_url(deal_name):
        product_urls = {
            "sunday": "https://catalog.paytm.com/sunday-bazaar-deals-llpid-78432",
            "super_value": "https://catalog.paytm.com/super-value-deals-02-llpid-141765",
            "super_market": "https://catalog.paytm.com/supermarket-shopnsave-llpid-115994",
            "world_store": "https://catalog.paytm.com/world-store-super-sale-llpid-115062",
        }
        return product_urls[deal_name]

    @staticmethod
    def get_query_string(page_number=1, sort_type="new"):
        sort_types = {
            "new": {
                "key": "sort_new",
                "value": 1
            },
            "popular": {
                "key": "sort_popular",
                "value": 1
            },
            "low_price": {
                "key": "sort_price",
                "value": 0
            },
            "high_price": {
                "key": "sort_price",
                "value": 1
            },
        }
        return {
            sort_types[sort_type]['key']: sort_types[sort_type]['value'],
            "page_count": page_number,
            "items_per_page": 30
        }

    @staticmethod
    def request_data(url, query_string):
        r = requests.get(url, params=query_string)
        if r.ok:
            data = r.json()
            return data
        print("Some issue with requesting the page.")
        return False

    @staticmethod
    def clean_data(data):
        grid_layout = data['grid_layout']
        products = []
        for data in grid_layout:
            product = {
                "id": data['product_id'],
                "name": data['name'],
                "raw_url": data['url'],
                "image_url": data['image_url'],
                "price": data['offer_price'],
                "link": "https://paytmmall.com/" + data['url'].split("/")[5].split("?")[0] + "-pdp",
                "new_url": data['newurl'],
                "discount": data['discount'],
                "offers": [],
                "categories": []
            }
            products.append(product)
        return products

    @staticmethod
    def get_offer_url(product_id):
        offer_base_url = "https://paytmmall.com/papi/v1/promosearch/product/%s/offers"
        return offer_base_url % product_id

    @staticmethod
    def get_sub_data(url, key, label):
        r = requests.get(url)
        if r.ok:
            data = r.json()
            if key in data:
                return data[key]
            print(f"Issue in retrieving the {label} ({key}) for the given product.")
            return False
        print(f"Issue in retrieving the {label} ({key}) for the given product.")
        return False

    def get_offers_data(self, url):
        return self.get_sub_data(url, key="codes", label="offers")

    def get_categories_data(self, url):
        return self.get_sub_data(url, key="ancestors", label="categories")

    @staticmethod
    def clean_offers_data(data):
        offers = []
        if not data:
            return []
        for given_offer in data:
            offer = {
                "code": given_offer['code'],
                "description": given_offer['offerText'],
                "valid_upto": parse(given_offer['valid_upto']).strftime("%Y-%m-%d %H:%M:%S"),
                "cashback": "".join([c for c in given_offer['code'] if 47 < ord(c) < 58])
            }
            if not offer['cashback']:
                offer['cashback'] = "0"
            if offer['code'] == "SHOP50" or offer['code'] == "MALL100":
                continue
            offers.append(offer)
        return offers

    @staticmethod
    def clean_categories_data(data):
        categories = []
        index = 0
        if not data:
            return []
        for given_category in data:
            category = {
                "id": given_category['id'],
                "name": given_category['name'],
                "seo_url": given_category['seourl'],
                "new_url": given_category['newurl'],
                "priority": index
            }
            index += 1
            categories.append(category)
        return categories

    @staticmethod
    def append_sub_data_to_product(product, offers, categories):
        product['offers'] = offers
        product['categories'] = categories

    def scrape(self, url, query_string):
        data = self.request_data(url, query_string)
        if data:
            print("Processing incoming data")
            products = self.clean_data(data)
            for product in products:
                print("Product with name %s about to process" % product['name'])
                sleep(2)
                offers_data = self.get_offers_data(self.get_offer_url(product['id']))
                categories_data = self.get_categories_data(product['new_url'])[:-1]
                if not offers_data:
                    continue
                if not categories_data:
                    continue
                offers = self.clean_offers_data(offers_data)
                categories = self.clean_categories_data(categories_data)
                print("Product with name %s processed" % product['name'])
                self.append_sub_data_to_product(product, offers, categories)
            return products
        return False

    def get_all_categories(self):
        url = "https://paytmmall.com/"
        xpath = '//*[@id="app"]/div/div[5]/div[5]/div[2]'
        r = requests.get(url)
        html_exp = self.find_by_xpath(r.text, xpath)
        elements = [element for element in html_exp[0].iterlinks()]
        self.all_categories = [{"name": element[0].text, "url": element[2]} for element in elements]
        return self

    @staticmethod
    def find_by_xpath(element_source, xpath_expression):
        root = html.fromstring(element_source)
        return root.xpath(xpath_expression)
