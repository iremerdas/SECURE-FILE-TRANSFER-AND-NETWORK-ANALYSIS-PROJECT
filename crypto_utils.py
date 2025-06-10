# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 00:02:00 2025

@author: Irem
"""

from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    return Fernet(key).encrypt(data)

def decrypt_data(data, key):
    return Fernet(key).decrypt(data)


