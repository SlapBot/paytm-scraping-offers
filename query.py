from core.db_manager import DB_Manager
from core.query_manager import QueryManager
import pprint


dbm = DB_Manager()
qm = QueryManager(dbm)
pp = pprint.PrettyPrinter(indent=4)

print("FOUND COUPON CODES: ")
pp.pprint(qm.get_distinct_coupon_codes())

print("FOUND PRODUCTS: ")
pp.pprint(qm.get_products_by_coupon_code("MALLLOOT60"))
