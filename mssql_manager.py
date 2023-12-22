import pymssql
import time
from collections import OrderedDict

class DatabaseManager:
    def __init__(self, server, user, password, database):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.cache = OrderedDict()
        self.cache_expiration = 60
        self.cache_limit = 100

    def connect(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, self.database)
        self.cursor = self.conn.cursor(as_dict=True)

    def disconnect(self):
        if self.conn:
            try:
                self.conn.close()
            except pymssql.OperationalError:
                pass  
            finally:
                self.conn = None
                self.cursor = None

    def is_connected(self):
        if self.conn:
            try:
                self.conn.cursor().execute("SELECT @@VERSION")
                return True
            except Exception:
                return False
        return False

    def execute_query(self, query):
        if query in self.cache:
            result, timestamp = self.cache[query]
            if time.time() - timestamp < self.cache_expiration:
                return result
        
        if len(self.cache) >= self.cache_limit:
            self.cache.popitem(last=False)
        
        try:
            if not self.is_connected():
                self.connect()
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.cache[query] = (result, time.time())  
            return result
        except Exception as e:
            self.connect()  # Create a new connection
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.cache[query] = (result, time.time())  
            return result


db_manager = DatabaseManager('<server IP or URL>', '<user>', '<password>', '<database name>')
