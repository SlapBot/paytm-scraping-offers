from db_manager import DB_Manager
from scrape import Scrape
from time import sleep

s = Scrape()
dbm = DB_Manager()

for i in range(3, 30):
    data = s.get_products_with_offers(s.get_url("super_market"), s.get_query_string(page_number=i+1, sort_type="popular"))
    print(data)
    dbm.insert_data(data)
    sleep(5)
