import socket
import time

# Create a socket object for communication using IPv4 and TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to all available network interfaces on port 26903
sock.bind(('0.0.0.0', 26903))

# Start listening for incoming connections, allowing one connection at a time
sock.listen(1)

# Print a message indicating the server is running
print("Server běží na portu 26903 ...")

# Infinite loop to handle incoming connections
while True:
    # Accept a new connection and get the connection object and client address
    conn, addr = sock.accept()
    print(f"Připojen: {addr}")  # Log the client's address

    try:
        # Record the current time for naming the received file
        time_revc = time.time()

        # Receive the header from the client (up to 1460 bytes)
        header = conn.recv(1460)
        print(header)  # Print the received header for debugging

        # Check if the header starts with "SIMG " (indicating an image transfer)
        if header.startswith(b"SIMG "):
            # Extract the size of the image from the header
            size = int(header[5:].strip())

            # Send an acknowledgment to the client
            conn.send(b"OK\n")
            print(f"Čekám na {size} bajtů...")  # Log the expected size of the image

            # Initialize a counter for the received bytes
            received = 0

            # Open a file to save the received image, using the timestamp in the filename
            with open(f"received_image{time_revc}.png", "wb") as f:
                # Loop until all bytes of the image are received
                while received < size:
                    # Receive data in chunks (up to 512 bytes or remaining size)
                    data = conn.recv(min(512, size - received))
                    if not data:
                        # If no data is received, the client may have disconnected
                        print("Spojení ukončeno klientem nebo došlo k chybě.")
                        conn.send(b"CANCEL\n")  # Notify the client of cancellation
                        break

                    # Write the received data to the file
                    f.write(data)

                    # Update the counter for received bytes
                    received += len(data)

                # Check if the entire image was received
                if received == size:
                    print("Obrázek přijat kompletně.")  # Log success
                    conn.send(b"DONE\n")  # Notify the client of successful transfer
                else:
                    print("Obrázek přijat jen částečně.")  # Log partial transfer

        else:
            # If the header is invalid, log an error message
            print("Neplatná hlavička")
    except Exception as e:
        # Handle any exceptions that occur during the connection
        print("Chyba:", e)
    finally:
        # Close the connection to the client
        conn.close()