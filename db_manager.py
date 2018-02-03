from datetime import datetime
import sqlite3


class DB_Manager(object):
    DATABASE_NAME = "scrapify"

    def __init__(self):
        self.conn = sqlite3.connect(DB_Manager.DATABASE_NAME)
        self.c = self.conn.cursor()

    def insert_data(self, data):
        products, offers = self.create_data(data)
        products_status = self.insert_products(products)
        offers_status = self.insert_offers(offers)
        if products_status and offers_status:
            return True
        return False

    def insert_products(self, data):
        self.c.executemany('''
        INSERT INTO products (product_uuid, name, raw_url, link, image_url, price, discount, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()
        return True

    def insert_offers(self, data):
        self.c.executemany('''
        INSERT INTO offers (product_uuid, code, description, cashback)
        VALUES (?, ?, ?, ?)
        ''', data)
        self.conn.commit()
        return True

    def create_data(self, products):
        products_data = []
        offers_data = []
        for product in products:
            products_data.append(self.create_product_data(product))
            offers_data.extend(self.create_offer_data(product))
        return products_data, offers_data

    @staticmethod
    def create_product_data(product):
        return (
            product['id'],
            product['name'],
            product['raw_url'],
            product['link'],
            product['image_url'],
            product['price'],
            int(product['discount']),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    @staticmethod
    def create_offer_data(product):
        offers_list = []
        for offer in product['offers']:
            offer_item = (
                product['id'],
                offer['code'],
                offer['description'],
                offer['cashback'],
            )
            offers_list.append(offer_item)
        return offers_list

    def close(self):
        self.c.close()
        return True
