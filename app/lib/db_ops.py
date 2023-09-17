from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

class DBOperations:
    def __init__(self):
        uri = os.getenv('MONGODB_SECRET')
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['horizon_v2']

    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error while pinging MongoDB: {e}")

    def insert_one(self, collection, data):
        try:
            return self.db[collection].insert_one(data)
        except Exception as e:
            print(f"Error while inserting data into {collection}: {e}")
            return None

    def find_one(self, collection, query):
        try:
            return self.db[collection].find_one(query)
        except Exception as e:
            print(f"Error while fetching data from {collection}: {e}")
            return None
        
    def find_many(self, collection, query={}, projection=None, limit=None, sort=None):
        if not query:
            raise ValueError("Must use with a query")
        try:
            cursor = self.db[collection].find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            if limit is not None:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error while fetching data from {collection}: {e}")
            return None
        
    def update_one(self, collection, filter, update):
        try:
            return self.db[collection].update_one(filter, update)
        except Exception as e:
            print(f"Error while updating data in {collection}: {e}")
            return None

    def close(self):
        if self.client:
            self.client.close()