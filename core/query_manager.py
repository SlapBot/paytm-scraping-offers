from core.db_manager import DB_Manager
from core.configurer import config


class QueryManager:
    def __init__(self, db_manager: DB_Manager):
        self.db_manager = db_manager

    @staticmethod
    def get_sql_from_filename(filename):
        abs_filename = config.get_abs_parent_directory() + "/sql_queries/" + filename
        with open(abs_filename, 'r') as sql_file:
            sql = sql_file.read()
        return sql

    def get_distinct_coupon_codes(self):
        sql = self.get_sql_from_filename("get_all_coupon_codes.sql")
        self.db_manager.cursor.execute(sql)
        return self.db_manager.cursor.fetchall()

    def get_products_by_coupon_code(self, coupon_code):
        sql = self.get_sql_from_filename("search_by_code.sql")
        self.db_manager.cursor.execute(sql.format(coupon_code))
        return self.db_manager.cursor.fetchall()
