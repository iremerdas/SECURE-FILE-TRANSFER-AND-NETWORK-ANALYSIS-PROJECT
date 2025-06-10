import socket
import hashlib
import os

def save_fragment(index, total, data, folder="fragments"):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"frag_{index}_of_{total}.bin"), "wb") as f:
        f.write(data)

def reassemble_file(total_fragments, folder="fragments", output_file="reassembled_file.txt"):
    with open(output_file, "wb") as out_file:
        for i in range(1, total_fragments + 1):
            frag_path = os.path.join(folder, f"frag_{i}_of_{total_fragments}.bin")
            with open(frag_path, "rb") as frag_file:
                out_file.write(frag_file.read())
    print(f"[✓] Dosya başarıyla yeniden oluşturuldu: {output_file}")

def sha256_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

# ============ SERVER MAIN =============

host = "127.0.0.1"
port = 9999

sock = socket.socket()
sock.bind((host, port))
sock.listen(1)

print("[🟢] Sunucu dinleniyor...")
conn, addr = sock.accept()
print(f"[+] Bağlantı: {addr}")

received_fragments = 0
expected_fragments = int(conn.recv(16).decode())
print(f"[i] Beklenen toplam fragment sayısı: {expected_fragments}")

while received_fragments < expected_fragments:
    metadata = conn.recv(16).decode()  # format: "3/5"
    index, total = map(int, metadata.split("/"))
    data = conn.recv(2048)
    save_fragment(index, total, data)
    received_fragments += 1
    print(f"[+] Fragment {index}/{total} alındı")

reassemble_file(expected_fragments)

# Hash doğrulama
received_hash = conn.recv(64).decode()
local_hash = sha256_checksum("reassembled_file.txt")
if received_hash == local_hash:
    print("[✓] SHA-256 hash doğrulandı.")
else:
    print("[✗] Hash eşleşmedi!")

conn.close()
sock.close()
