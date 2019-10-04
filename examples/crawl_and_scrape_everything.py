"""
This snippet only written so
that example scripts can be run standalone within their sub-directory: python examples/crawl_and_scrape_category.py
Don't do it this way when importing from outside the repository as you should.
Simply remove the passage from start to end tags

Start Snippet
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
This snippet only written so 
that example scripts can be run standalone within their sub-directory: python examples/crawl_and_scrape_category.py
Don't do it this way when importing from outside the repository as you should.
Simply remove the passage from start to end tags

End Snippet
"""

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
