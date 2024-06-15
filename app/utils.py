from cryptography.fernet import Fernet
import base64
from config import Config

config = Config()
client = config.CLIENT
uri = config.URI
db = client["encryptedictkey"]

def data_encrypt(data, user_id):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    key_b64 = base64.b64encode(key).decode('utf-8')
    encrypted_dict = {
            'encrypted_data': encrypted_data_b64,
            'key': key_b64,
            'user_id': user_id,
            }
    return encrypted_dict

def data_decrypt(encrypted_dict, data):
    key_64 = encrypted_dict['key']
    data = data
    print("data in data_decrypt function: ", data)
    key = base64.b64decode(key_64)
    f = Fernet(key)
    encrypted_data = base64.b64decode(data)
    data = f.decrypt(encrypted_data)
    print(" data: ", data)
    return data


def dict_to_mongodb(user_dict, username):
    collection_name = db[username]
    collection_name.insert_one(user_dict)
    print("dict added to ", username)

def decrypt_mongodb(userid, collection):
    print("before en_dict query")
    col = db[collection]
    print("col is: ", col, " collection is: ", collection)
 
    en_dict = col.find_one({})
    print("after en_dict query", en_dict)
    return en_dict
     
