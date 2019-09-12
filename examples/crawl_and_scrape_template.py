from core.db_manager import DB_Manager
from core.scrape import Scrape
from time import sleep

s = Scrape()
categories = s.get_all_categories()
dbm = DB_Manager()

page_start = 0
page_end = 30

# Loop to fetch pages from start to end.
for i in range(page_start, page_end):
    # Write your own logic to meet the needs of your scraping requirements.

    print("Crawling and Scraping for Category: %s" % categories[0]['name'])
    data = s.scrape(categories[0]['url'], s.get_query_string(page_number=i + 1, sort_type="popular"))

    # insert the scraped data to a database.

    dbm.insert_data(data)

    # sleep to avoid rate limiting.

    sleep(5)
