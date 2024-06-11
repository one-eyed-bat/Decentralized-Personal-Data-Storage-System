from pymongo.mongo_client import MongoClient
from pymongo_get_database import get_database
from pymongo.server_api import ServerApi

dbname = get_database()
uri = "mongodb+srv://michael:mikol123@encryptedictkey.cfoypkc.mongodb.net/?retryWrites=true&w=majority&appName=encryptedictkey"
collection_name = dbname['user_1_dict']
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
