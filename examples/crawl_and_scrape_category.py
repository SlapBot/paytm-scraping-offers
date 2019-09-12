from core.db_manager import DB_Manager
from core.scrape import Scrape
from time import sleep

s = Scrape()
categories = s.get_all_categories()
dbm = DB_Manager()

# print(categories) -> Will show you all the available categories in paytm mall.
# crawl and scrape category: Speakers -> existing at 3rd index position of categores list.

for i in range(0, 30):
    print("Crawling and Scraping for Category: %s" % categories[3]['name'])
    data = s.scrape(categories[3]['url'], s.get_query_string(page_number=i + 1, sort_type="popular"))
    dbm.insert_data(data)
    sleep(5)
