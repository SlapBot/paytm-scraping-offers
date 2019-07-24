import MySQLdb
import MySQLdb.cursors
from datetime import datetime
from configurer import config


class DB_Manager(object):
    PRODUCTS_TABLE_KEY = "products_table_name"
    OFFERS_TABLE_KEY = "offers_table_name"
    CATEGORIES_TABLE_KEY = "categories_table_name"
    PRODUCT_OFFER_PIVOT_TABLE_KEY = "product_offer_pivot_table_name"
    PRODUCT_CATEGORY_PIVOT_TABLE_KEY = "product_category_pivot_table_name"

    def __init__(self):
        self.config = config
        self.cnx = MySQLdb.connect(user=config.get_configuration('user'),
                                   passwd=config.get_configuration('password'),
                                   host=config.get_configuration('host'),
                                   db=config.get_configuration('database_name'),
                                   cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.cnx.cursor()

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.cursor.close()
        self.cnx.close()
        return True

    def insert_data(self, data):
        products, offers, categories = self.create_data(data)
        products_status = self.insert_products(products)
        offers_status = self.insert_offers(offers)
        categories_status = self.insert_categories(categories)
        if any((products_status, offers_status, categories_status)):
            self.link_pivots(data)
        return False

    def create_data(self, products):
        products_data = []
        offers_data = []
        categories_data = []
        for product in products:
            products_data.append(self.create_product_data(product))
            offers_data.extend(self.create_offer_data(product['offers']))
            categories_data.extend(self.create_categories_data(product['categories']))
        return products_data, offers_data, categories_data

    def insert_products(self, data):
        column_keys = self.get_columns_from_table_name(self.PRODUCTS_TABLE_KEY)
        return self.insert_many_sql_query(self.PRODUCTS_TABLE_KEY, column_keys, data)

    def insert_offers(self, data):
        column_keys = self.get_columns_from_table_name(self.OFFERS_TABLE_KEY)
        return self.insert_many_sql_query(self.OFFERS_TABLE_KEY, column_keys, data, primary_key=False)

    def insert_categories(self, data):
        column_keys = self.get_columns_from_table_name(self.CATEGORIES_TABLE_KEY)
        return self.insert_many_sql_query(self.CATEGORIES_TABLE_KEY, column_keys, data)

    def link_pivots(self, data):
        offers_pivot_data, categories_pivot_data = self.create_pivot_data(data)
        self.link_offers(offers_pivot_data)
        self.link_categories(categories_pivot_data)

    def get_columns_from_table_name(self, table_name_key):
        table_name = self.config.get_configuration(table_name_key, "TABLE")
        self.cursor.execute("SHOW COLUMNS FROM %s" % table_name)
        return [data['Field'] for data in self.cursor.fetchall()]

    def insert_many_sql_query(self, table_name_key, column_keys, data, primary_key=True):
        table_name = self.config.get_configuration(table_name_key, "TABLE")
        if primary_key:
            columns = ', '.join(column_keys)
            values = ", ".join(["%s" for i in range(len(data[0]))])
        else:
            columns = ', '.join(column_keys[1:])
            values = ", ".join(["%s" for i in range(len(data[0]))])
        sql = "IGNORE INSERT INTO " + table_name + " (" + columns + ") VALUES (" + values + ")"
        print(sql)
        try:
            self.cursor.executemany(sql, data)
            self.cnx.commit()
        except Exception as e:
            print(e)
        return True

    def insert_one_sql_query(self, table_name_key, column_keys, data, primary_key=True):
        table_name = self.config.get_configuration(table_name_key, "TABLE")
        if primary_key:
            columns = ', '.join(column_keys)
            values = ", ".join(["%s" for i in range(len(data[0]))])
        else:
            columns = ', '.join(column_keys[1:])
            values = ", ".join(["%s" for i in range(len(data[0]))])
        sql = "INSERT INTO " + table_name + " (" + columns + ") VALUES (" + values + ")"
        print(sql)
        for query in data:
            try:
                self.cursor.execute(sql, query)
                self.cnx.commit()
            except Exception as e:
                print(e)
        return True

    def create_pivot_data(self, products):
        offers_pivot_data = []
        categories_pivot_data = []
        existing_offers = self.get_all_existing_offers(self.OFFERS_TABLE_KEY)
        for product in products:
            for offer in product['offers']:
                # TODO: sort out offer unique_id problem somehow
                offer_id = next(
                    existing_offer['id'] for existing_offer in existing_offers
                    if existing_offer['code'] == offer['code']
                )
                offers_pivot_data.append((product['id'], offer_id))
            for category in product['categories']:
                categories_pivot_data.append((product['id'], category['id']))
        return offers_pivot_data, categories_pivot_data

    def link_offers(self, data):
        column_keys = self.get_columns_from_table_name(self.PRODUCT_OFFER_PIVOT_TABLE_KEY)
        return self.insert_many_sql_query(self.PRODUCT_OFFER_PIVOT_TABLE_KEY, column_keys, data, primary_key=False)

    def link_categories(self, data):
        column_keys = self.get_columns_from_table_name(self.PRODUCT_CATEGORY_PIVOT_TABLE_KEY)
        return self.insert_many_sql_query(self.PRODUCT_CATEGORY_PIVOT_TABLE_KEY, column_keys, data, primary_key=False)

    def get_all_existing_offers(self, table_name_key):
        table_name = self.config.get_configuration(table_name_key, "TABLE")
        self.cursor.execute('SELECT `id`, `code` FROM `%s`' % table_name)
        num_rows = self.cursor.rowcount
        print("Total Offers: {}".format(num_rows))
        rows = self.cursor.fetchall()
        if self.cursor.rowcount == 0:
            exit("No offers present")
        return rows

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
    def create_offer_data(offers):
        offers_list = []
        for offer in offers:
            offer_item = (
                offer['code'],
                offer['description'],
                offer['valid_upto'],
                offer['cashback']
            )
            offers_list.append(offer_item)
        return offers_list

    @staticmethod
    def create_categories_data(categories):
        categories_list = []
        for category in categories:
            category_item = (
                category['id'],
                category['name'],
                category['seo_url'],
                category['new_url'],
                category['priority']
            )
            categories_list.append(category_item)
        return categories_list
