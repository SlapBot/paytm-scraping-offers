from core.db_manager import DB_Manager
from core.migrator import Migrator


dbm = DB_Manager()
m = Migrator(dbm)

m.migrate()
