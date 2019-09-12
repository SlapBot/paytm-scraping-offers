from core.db_manager import DB_Manager
from core.scrape import Scrape
from time import sleep

s = Scrape()
categories = s.get_all_categories()
dbm = DB_Manager()

for category in categories[3:]:
    for i in range(0, 1):
        print("Crawling and Scraping for Category: %s" % category['name'])
        data = s.scrape(category['url'], s.get_query_string(page_number=i + 1, sort_type="popular"))
        dbm.insert_data(data)
        sleep(5)
