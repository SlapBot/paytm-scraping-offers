import requests

def get_url(deal_name):
    product_urls = {
        "sunday": "https://catalog.paytm.com/sunday-bazaar-deals-llpid-78432",
        "super_value": "https://catalog.paytm.com/super-value-deals-02-llpid-141765",
        "super_market": "https://catalog.paytm.com/supermarket-shopnsave-llpid-115994"
    }
    return product_urls[deal_name]

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

def request_data(url, query_string):
    r = requests.get(url, params=query_string)
    if r.ok:
        data = r.json()
        return data
    print("Some issue with requesting the page.")
    return False

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
            "offers": []
        }
        products.append(product)
    return products

def get_offer_url(product_id):
    offer_base_url = "https://paytmmall.com/papi/v1/promosearch/product/%s/offers"
    return offer_base_url % product_id

def get_offers_data(url):
    r = requests.get(url)
    if r.ok:
        data = r.json()
        if 'codes' in data:
            return data['codes']
        print("Issue in retrieving the offers for the given product.")        
        return False
    print("Issue in retrieving the offers for the given product.")
    return False

def clean_offers_data(data):
    offers = []
    if not data:
        return []
    for given_offer in data:
        offer = {
            "code": given_offer['code'],
            "description": given_offer['offerText']
        }
        offers.append(offer)
    return offers

def append_offers_to_product(product, offers):
    product['offers'] = offers

def get_products_with_offers(url, query_string):
    data = request_data(url, query_string)
    if data:
        products = clean_data(data)[:5]
        for product in products:
            offers_data = get_offers_data(get_offer_url(product['id']))
            if not offers_data:
                continue
            offers = clean_offers_data(offers_data)
            append_offers_to_product(product, offers)
        return products
    return False

if __name__ == "__main__":
    data = get_products_with_offers(get_url("super_value"), get_query_string())
    print(data)
