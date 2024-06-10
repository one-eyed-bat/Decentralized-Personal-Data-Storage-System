from cryptography.fernet import Fernet
import base64


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





