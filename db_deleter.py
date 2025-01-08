
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

##### ADD URI #######







# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database_name="CITcluster0"
collection_name="Collection_1"
db = client[database_name]
collection = db[collection_name]

collections = db.list_collection_names()
print(f"Collections found in database '{database_name}': {collections}")

############ DROP DATABASES ############
############ keep commented ############

try: 
    for collection in collections:
        db[collection].drop()
        print(f"Collection '{collection}' has been dropped.")
        
except Exception as e:
    print(f"An error occurred: {e}")
    
    