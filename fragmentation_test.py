# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 01:44:27 2025

@author: Irem
"""

from scapy.all import IP, UDP, send

# Uzun veri
data = b"A" * 4000  # 4000 byte'lık veri

# Fragmentation ayarları
packet1 = IP(dst="127.0.0.1", id=12345, flags=1, frag=0) / UDP(dport=1234, sport=1234) / data[:1480]
packet2 = IP(dst="127.0.0.1", id=12345, flags=1, frag=185) / data[1480:2960]
packet3 = IP(dst="127.0.0.1", id=12345, flags=0, frag=370) / data[2960:]

# Gönder
send(packet1)
send(packet2)
send(packet3)

print("Parçalanmış paketler gönderildi.")
