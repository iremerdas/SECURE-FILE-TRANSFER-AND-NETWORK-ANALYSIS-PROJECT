# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 00:01:38 2025

@author: Irem
"""

import socket
from crypto_utils import encrypt_data, generate_key
from hash_utils import calculate_hash
from rsa_utils import encrypt_key_rsa
from cryptography.hazmat.primitives import serialization

# Dosyayı oku
with open("gonderilecek_dosya.txt", "rb") as f:
    file_data = f.read()

file_hash = calculate_hash(file_data)

with socket.socket() as client:
    client.connect(('127.0.0.1', 9999))

    # Sunucunun public key'ini al
    public_pem = client.recv(1024)
    public_key = serialization.load_pem_public_key(public_pem)

    # AES key üret ve RSA ile şifrele
    aes_key = generate_key()
    encrypted_aes_key = encrypt_key_rsa(public_key, aes_key)
    client.send(encrypted_aes_key)

    # Dosyayı AES ile şifrele
    encrypted = encrypt_data(file_data, aes_key)

    # Hash + Şifreli dosyayı gönder
    client.send(file_hash.encode())
    client.sendall(encrypted)

    print("Dosya gönderildi.")
