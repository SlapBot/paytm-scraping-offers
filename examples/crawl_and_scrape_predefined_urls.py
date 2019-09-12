from core.db_manager import DB_Manager
from core.scrape import Scrape
from time import sleep

s = Scrape()
dbm = DB_Manager()

for i in range(0, 30):
    data = s.scrape(s.get_predefined_url("super_market"), s.get_query_string(page_number=i + 1, sort_type="popular"))
    dbm.insert_data(data)
    sleep(5)

for i in range(0, 30):
    data = s.scrape(s.get_predefined_url("sunday"), s.get_query_string(page_number=i + 1, sort_type="popular"))
    dbm.insert_data(data)
    sleep(5)

for i in range(0, 30):
    data = s.scrape(s.get_predefined_url("super_value"), s.get_query_string(page_number=i + 1, sort_type="popular"))
    dbm.insert_data(data)
    sleep(5)

for i in range(0, 30):
    data = s.scrape(s.get_predefined_url("world_store"), s.get_query_string(page_number=i + 1, sort_type="popular"))
    dbm.insert_data(data)
    sleep(5)
