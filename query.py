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
