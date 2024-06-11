from cryptography.fernet import Fernet
import base64
from pymongo_get_database import get_database
from config import Config

config = Config()
client = config.CLIENT
def data_encrypt(data, user_id):
    key = Fernet.generate_key()
    f = Fernet(key)

    data_type ='text' if isinstance(data, str) else 'bytes'
    if data_type == 'text':
        data = data.encode('utf-8')
    encrypted_data = f.encrypt(data)
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    key_b64 = base64.b64encode(key).decode('utf-8')
    encrypted_dict = {
            'encrypted_data': encrypted_data_b64,
            'key': key_b64,
            'type': data_type,
            'user_id': user_id,
            }
    return encrypted_dict

def data_decrypt(encrypted_dict):
    key_64 = encrypted_dict['key']
    data  = encrypted_dict['encrypted_data']
    data_type = encrypted_dict['type']
    key = base64.b64decode(key_64)
    f = Fernet(key)
    encrypted_data = base64.b64decode(data)
    data = f.decrypt(encrypted_data)
    if data_type == 'text':
        data = data.decode('utf-8')
    return data
    pass

def dict_to_mongodb(user_dict, username):
    dbname = get_database()
    collection_name = dbname[username]
    collection_name.insert_one(user_dict)
    print("dict added to ", username)
    return dbname

def decrypt_mongodb(userid, collection):
    #user_id = {"user_id": userid}
    print("before en_dict query")
    db = client["encryptedictkey"]
    col = db[collection]
     
    en_dict = col.find({}, {"_id": 0, "encrypted_data" : 1,  "type": 1})
    print("after en_dict query", en_dict)
    for data in en_dict:
        print("at decrypt_mongodb function, data is: ", data)
    
