# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 00:01:11 2025

@author: Irem
"""

import socket
from crypto_utils import decrypt_data
from hash_utils import verify_hash
from rsa_utils import generate_keys, decrypt_key_rsa
from cryptography.hazmat.primitives import serialization

# RSA anahtar çifti üret
private_key, public_key = generate_keys()

with socket.socket() as server:
    server.bind(('0.0.0.0', 9999))
    server.listen(1)
    print("Sunucu dinleniyor...")

    conn, addr = server.accept()
    with conn:
        print(f"{addr} bağlandı.")

        # Public key'i istemciye gönder
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        conn.send(public_pem)

        # Şifreli AES anahtarını al ve çöz
        encrypted_aes_key = conn.recv(512)
        aes_key = decrypt_key_rsa(private_key, encrypted_aes_key)

        # Dosya hash'ini al
        hash_value = conn.recv(64).decode()

        # Şifreli dosyayı al
        encrypted_data = b''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            encrypted_data += data

        # AES ile çöz
        decrypted = decrypt_data(encrypted_data, aes_key)

        # SHA-256 hash doğrulama
        if verify_hash(decrypted, hash_value):
            with open("gelen_dosya.txt", "wb") as f:
                f.write(decrypted)
            print("Dosya alındı ve doğrulandı.")
        else:
            print("HATA: Bütünlük kontrolü başarısız!")


"""
import socket
from crypto_utils import decrypt_data
from hash_utils import verify_hash
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

with socket.socket() as server:
    server.bind(('0.0.0.0', 9999))
    server.listen(1)
    print("Sunucu dinleniyor...")

    conn, addr = server.accept()
    with conn:
        print(f"{addr} bağlandı.")
        conn.send(key)

        hash_value = conn.recv(64).decode()
        encrypted_data = b''

        while True:
            data = conn.recv(1024)
            if not data:
                break
            encrypted_data += data

        decrypted = decrypt_data(encrypted_data, key)

        if verify_hash(decrypted, hash_value):
            with open("gelen_dosya.txt", "wb") as f:
                f.write(decrypted)
            print("Dosya alındı ve doğrulandı.")
        else:
            print("HATA: Bütünlük kontrolü başarısız!")
"""


