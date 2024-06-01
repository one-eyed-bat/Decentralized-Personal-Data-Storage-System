from cryptography.fernet import Fernet
import base64




def data_encrypt(data):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    data_type ='text' if isinstance(data, str) else 'bytes'
    if data_type == 'text':
        data = data.encode('utf-8')
    encrypted_data = cipher_suite.encrypt(data)
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    key_b64 = base64.b64encode(key).decode('utf-8')
    encrypted_dict = {
            'encrypted_data': encrypted_data_b64,
            'key': key_b64,
            'type': data_type
            }
    return encrypted_dict

def data_decrypt(encrypted_dict):
    pass





