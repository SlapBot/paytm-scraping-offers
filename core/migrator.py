from core.db_manager import DB_Manager
from core.configurer import config


class Migrator:
    def __init__(self, db_manager: DB_Manager):
        self.db_manager = db_manager
        self.migration_filename = config.get_abs_parent_directory() + "/sql_queries/migrations.sql"

    def migrate(self):
        with open(self.migration_filename) as sql_file:
            sql = sql_file.read()
        self.db_manager.cursor.execute(sql)
        self.db_manager.close()
        print("Database Migrated Successfully.")
        return True
