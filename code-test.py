from cryptography.fernet import Fernet


key = Fernet.generate_key()
fernet = Fernet(key)



def encrypt(text):
    cipher = fernet.encrypt(text.encode())
    print(cipher)
    return cipher


def decrypt(cipher):
    decipher = fernet.decrypt(cipher).decode()
    print(decipher)


message = "hello world"
print(message)
cipher = encrypt(message)
decrypt(cipher)