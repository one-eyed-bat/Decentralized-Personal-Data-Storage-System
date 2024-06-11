from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_database():
    CONNECTION_STRING = 'mongodb+srv://michael:mikol123@encryptedictkey.cfoypkc.mongodb.net/?retryWrites=true&w=majority&appName=encryptedictkey'
    client = MongoClient(CONNECTION_STRING)

    return client['user_dicts']

if __name__ == "__main__":
    dbname = get_database()


