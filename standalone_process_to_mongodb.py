
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
    
    
    
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    

file_path="req.txt"
manual_title="fichier1"

with open(file_path, "r") as file:
    for line in file:
        content = line.strip()  # Remove leading and trailing whitespace
        if content:  # Only process non-empty lines
            document = {
                "title": manual_title,
                "content": content,
                "timestamp": datetime.utcnow()  # Automatically generate a timestamp
            }
            collection.insert_one(document)  # Insert into MongoDB

print("File data successfully pushed to MongoDB!")