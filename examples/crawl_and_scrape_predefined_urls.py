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
