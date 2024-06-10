from utils import data_encrypt, data_decrypt

string = 'this is a test string'
encrypt = data_encrypt(string, 1)
print(encrypt)

decrypted = data_decrypt(encrypt)
print(decrypted)
