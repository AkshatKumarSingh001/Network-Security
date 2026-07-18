from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

username = "akshatsingh360_db_user"
password = quote_plus("Oon3qYAl1N5El8WL")  # encodes any special chars safely

uri = f"mongodb+srv://{username}:{password}@cluster0.owvksc7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)