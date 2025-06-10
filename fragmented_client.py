import socket
import os
import hashlib
import time

def split_file(file_path, fragment_size=1024):
    with open(file_path, "rb") as f:
        data = f.read()
    fragments = [data[i:i + fragment_size] for i in range(0, len(data), fragment_size)]
    return fragments

def sha256_checksum(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

# ============ CLIENT MAIN =============

host = "127.0.0.1"
port = 9999
file_path = r"C:\Users\Irem\OneDrive - Bursa Teknik Universitesi\Belgeler\OKUL\4.sinif\Donem_2\bil_ag\guvenli_dosya_transferi_projesi\ornek.txt"  # gönderilecek dosya

# 1. Dosyayı parçala
fragments = split_file(file_path)
total = len(fragments)
print(f"[i] Toplam {total} fragment oluşturuldu.")

# 2. Soket aç
sock = socket.socket()
sock.connect((host, port))

# 3. Toplam fragment sayısını gönder
sock.send(str(total).zfill(16).encode())  # örn: "0000000000000005"

# 4. Her fragment'ı sırayla gönder
for index, frag in enumerate(fragments, start=1):
    metadata = f"{index}/{total}".zfill(16).encode()  # örn: "0000000000003/5"
    sock.send(metadata)
    time.sleep(0.05)  # biraz bekletme, paket çakışmasını azaltır
    sock.send(frag)
    print(f"[→] Fragment {index}/{total} gönderildi")

# 5. SHA-256 gönder
full_data = b''.join(fragments)
hash_value = sha256_checksum(full_data)
sock.send(hash_value.encode())
print("[✓] SHA-256 gönderildi.")

sock.close()
