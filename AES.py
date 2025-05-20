from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt_file(key, in_filename, out_filename):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(in_filename, 'rb') as f:
        plaintext = pad(f.read())
    iv = cipher.iv
    ciphertext = cipher.encrypt(plaintext)
    with open(out_filename, 'wb') as f:
        f.write(iv + ciphertext)

def decrypt_file(key, in_filename, out_filename):
    with open(in_filename, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ciphertext)
    with open(out_filename, 'wb') as f:
        f.write(plaintext.rstrip(b"\0"))

# Usage
key = get_random_bytes(16)  # Save this key securely!
encrypt_file(key, 'secret.txt', 'secret.enc')
# On unlock gesture:
decrypt_file(key, 'secret.enc', 'secret_decrypted.txt')