# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 01:28:03 2025

@author: Irem
"""

from scapy.all import IP, TCP, send

# Hedef IP (kendine test yapıyorsan 127.0.0.1)
target_ip = "127.0.0.1"

# IP başlığına elle müdahale
packet = IP(dst=target_ip, ttl=42, flags='DF') / TCP(dport=80, flags='S')

# Checksum manuel bırakılırsa Scapy hesaplar; istersen elle atayabilirsin:
# packet.chksum = 0x1234  # örnek checksum

packet.show()  # Paket yapısını göster
send(packet)   # Paketi gönder

print("Paket gönderildi!")
