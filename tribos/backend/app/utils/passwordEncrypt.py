import hashlib


# Função responsável por encriptar as senhas do sistema
def password_encrypt(password):
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()
