# Paytm Scraping Offers

A framework to crawl and scrape all of the [PaytmMall](https://paytmmall.com) products
and their associated information (categories, coupons, etc) and save them in a relational database (MySQL)
with an extended well-defined API to control the workflow of crawling and scraping.

- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
    - [Pre-Requisites](#pre-requisites)
    - [Application Setup](#application-setup)
    - [System Setup](#system-setup)
- [Getting Started](#getting-started)
    - [Scraping](#scraping)
    - [Querying](#querying)
- [Usage](#usage)
    - [Advanced API](#advanced-api)
- [Applications](#applications)
- [Why?](#why)

## Motivation

- Paytm Mall doesn't provides you with a feature of searching/querying products on the basis of some coupon-code (obviously).

- So I took it upon myself to crawl and scrape all of their products
and interlink each of their offers with their given products. Result of doing so?

![](https://github.com/SlapBot/paytm-scraping-offers/blob/master/screenshots/1.gif)

- I found some of their hidden steal deals giving me discount of as much as 100% in certain cases which
I ended up giving many of the steal products for free to the people in need that I bought for effectively free.

## Features

- Crawl and scrape all of the products from paytm-mall app.
- Data stored in DBMS for effective retrieval by writing powerful SQL queries.
- Batch retrieval and Batch Multi-Insert.
- Can be ported to async requests by using a library like asyncio with ease (but need to use proxies to avoid getting rate-limited)
- Find steal-deals by searching products on the basis of coupon-codes (Search all products with coupon-code, FMCGSAVE45 for example)

![](https://github.com/SlapBot/paytm-scraping-offers/blob/master/screenshots/2.gif)

## Installation

### Pre-requisites

1. Python3
2. pip
3. virtualenv

### Application Setup

1. Clone the repo: `git clone https://github.com/slapbot/paytm-scraping-offers`
2. Cd into the directory: `cd paytm-scraping-offers`
3. Create a virtualenv for python: `virtualenv paytm-scraping-offers-env`
4. Activate the virtualenv:
    - Linux: `source paytm-scraping-offers-env/bin/activate`
    - Windows: `sources paytm-scraping-offers-env/Scripts/activate`
5. Upgrade your pip to latest version: pip install --upgrade pip
6. Install the application dependencies: `pip install -r requirements.txt`

### System Setup

1. Install MySQL dependencies depending on your OS: https://dev.mysql.com/downloads/installer/
2. Create a database
3. Plug in the configuration of MySQL you've just setup at: `config.ini`
4. Run `python migrate.py` to migrate the database with correct tables.

![](https://github.com/SlapBot/paytm-scraping-offers/blob/master/screenshots/3.gif)

## Getting Started

### Scraping

```
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

```

- Run `python examples/crawl_and_scrape_category.py` to scrape away all of the products with their steal deals from `speakers` category
- Run `python examples/crawl_and_scrape_everything.py` to scrape away all of the products listed in Paytm Mall.
- Run `python examples/crawl_and_scrape_predefined_urls.py` to scrape away all of the products of a given offer going (Super Sunday) etc.
- Run `python examples/crawl_and_scrape_template.py` to get an understanding of how to create your own scrapers.

### Querying

```
from core.db_manager import DB_Manager
from core.query_manager import QueryManager
import pprint


dbm = DB_Manager()
qm = QueryManager(dbm)
pp = pprint.PrettyPrinter(indent=4)

print("FOUND COUPON CODES: ")

coupon_codes = qm.get_distinct_coupon_codes()
pp.pprint(coupon_codes)

coupon_code = coupon_codes[0]['code']

print("FOUND PRODUCTS FOR COUPON CODE {0}: ".format(coupon_code))
pp.pprint(qm.get_products_by_coupon_code(coupon_code))

```

- Run `python query.py` to query results from what you've scraped.

## Usage

The API is super straightforward and intuitive to understand and consume, 
taking a look at the `examples` should simply tell you all about the basics of the workflow of the framework.

A classic scraper might look like this:

```
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

```

### Advanced API

- `core/configurer.py`: Managing configuration of the application by retrieving information from `config.ini` file.
- `core/db_manager.py`: Abstraction over database query calls spread across the application.
- `core/migrator.py`: Using `db_manager.py` to create migrations that you do while installing the project.
- `core/query_manager.py`: Another consumer of `db_manager.py` to showcase SQL queries of various kinds.
- `core/scrape.py`: Responsible to scrape the paytm products.
- `sql_queries`: Some SQL queries that might come super handy to use and get an overview of how to write your own.

## Applications

- Scraping offers coupons and getting some of the best steal-deals
- Creating a database of products, categories, prices, discounts, reviews to create ML models.
- Analysis of products listed by paytm-mall compared to amazon, flipkart and e-commerce alternatives.
- And your imagination to consume data for any kind of analytics or visualisation.

## Why?

Its one of the projects that I wrote quite back when Paytm-Mall had just started and I've already 
bought enough steal-deals for myself ranging me discounts from (60-100% yes 100%). But I've 
recently embraced a minimalistic lifestyle so the project is no longer needed for my interests.

So I've figured to make the code open-source for anyone to create a database, find steal-deals, 
create comparison aggregator of various e-commerce websites, etc.
