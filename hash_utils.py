    # -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 00:02:16 2025

@author: Irem
"""

import hashlib

def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()

def verify_hash(data, expected_hash):
    return calculate_hash(data) == expected_hash
