import socket
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 26903))
sock.listen(1)

print("Server běží na portu 26903 ...")

while True:
    conn, addr = sock.accept()
    print(f"Připojen: {addr}")
    try:
        #header = conn.recv(1460)
        time_revc = time.time()
        header = conn.recv(1460)
        print(header)
        #while not header.endswith(b'\n'):
        #    header += conn.recv(1460)
        #    print(header)    
        if header.startswith(b"SIMG "):
            size = int(header[5:].strip())
            conn.send(b"OK\n")
            print(f"Čekám na {size} bajtů...")

            received = 0
            with open(f"received_image{time_revc}.png", "wb") as f:
                while received < size:
                    data = conn.recv(min(512, size - received))
                    if not data:
                        print("Spojení ukončeno klientem nebo došlo k chybě.")
                        conn.send(b"CANCEL\n")
                        break
                    f.write(data)
                    received += len(data)

                if received == size:
                    print("Obrázek přijat kompletně.")
                    conn.send(b"DONE\n")
                else:
                    print("Obrázek přijat jen částečně.")

            
        else:
            print("Neplatná hlavička")
    except Exception as e:
        print("Chyba:", e)
    finally:
        conn.close()