import machine  # Import the machine module for hardware interaction
import time  # Import the time module for delays
import BG77  # Import the BG77 module (likely for communication with a BG77 modem)
import os  # Import the os module for file operations
import dl_sdcard_comm  # Import a custom module for SD card communication

# Function to toggle the state of an LED
def toggle(led):
    if led == 1:
        led = 0  # Turn off the LED if it's on
    else:
        led = 1  # Turn on the LED if it's off
    return led

# Function to send an image file over a socket
def send_img(bgsocket, led7, random_num):
    rootimg = '/image' + str(random_num) + '.png'  # Construct the image file path
    try:
        capt_img = open('/sd/image4.png', 'rb')  # Open the image file in binary read mode
    except:
        print('chyba otevření img4.png')  # Print an error message if the file can't be opened
    filesize = os.stat(rootimg)[6]  # Get the file size in bytes
    header = f"SIMG {filesize}"  # Create a header with the file size
    while True:
        packet = capt_img.read(512)  # Read the file in chunks of 512 bytes
        endof_file = False
        if not packet:
            print('End of file reached')  # Indicate the end of the file
            endof_file = True
            break

        if endof_file == False:
            print('Sending packet...')  # Indicate that a packet is being sent
            print(len(packet))  # Print the size of the packet
            bgsocket.send(packet)  # Send the packet over the socket

            time.sleep(0.1)  # Delay for stability
            toggle(led7.value())  # Toggle the LED state
            time.sleep(0.1)  # Delay for stability
            toggle(led7.value())  # Toggle the LED state again

# Improved version of the send_img function with acknowledgment handling
def send_imgv2(bgsocket, led7, random_num):
    rootimg = '/image' + str(random_num) + '.png'  # Construct the image file path
    capt_img = open('/sd/image4.png', 'rb')  # Open the image file in binary read mode
    filesize = os.stat(rootimg)[6]  # Get the file size in bytes

    header = f"SIMG {filesize}\n"  # Create a header with the file size
    bgsocket.send(header)  # Send the header over the socket
    
    ack = bgsocket.recv(10)  # Wait for acknowledgment from the server
    acke = ack[1]  # Extract the acknowledgment message
    print(acke)
    if acke is None or "OK" not in acke:  # Check if acknowledgment is valid
        print("Header error/ Wrong server error")  # Print an error message
        capt_img.close()  # Close the file
        return
    
    while True:
        packet = capt_img.read(512)  # Read the file in chunks of 512 bytes
        endof_file = False
        if not packet:
            print('End of file reached')  # Indicate the end of the file
            endof_file = True
            break

        if endof_file == False:
            print('Sending packet...')  # Indicate that a packet is being sent
            print(len(packet))  # Print the size of the packet
            bgsocket.sendBytes(packet)  # Send the packet over the socket

            time.sleep(0.1)  # Delay for stability
            toggle(led7.value())  # Toggle the LED state
            time.sleep(0.1)  # Delay for stability
            toggle(led7.value())  # Toggle the LED state again

    done = bgsocket.recv(10)  # Wait for a "DONE" message from the server
    donee = done[1]  # Extract the "DONE" message
    print(donee)
    if 'DONE' in donee:  # Check if the transfer was successful
        print("Obrázek úspěšně odeslán.")  # Print a success message
    else:
        print("Přenos selhal nebo neúplný.")  # Print a failure message
    capt_img.close()  # Close the file

# Experimental version of the send_img function with additional button handling
def send_imgv3(bgsocket, led7, random_num):
    button0 = machine.Pin(6, machine.Pin.IN)  # Initialize a button on pin 6
    b_value = button0.value()  # Get the button's current state
    
    rootimg = '/image' + str(random_num) + '.png'  # Construct the image file path
    capt_img = open('/sd/image4.png', 'rb')  # Open the image file in binary read mode
    filesize = os.stat(rootimg)[6]  # Get the file size in bytes

    header = f"SIMG {filesize}\n"  # Create a header with the file size
    bgsocket.send(header)  # Send the header over the socket
    
    ack = bgsocket.recv(10)  # Wait for acknowledgment from the server
    acke = ack[1]  # Extract the acknowledgment message
    print(ack)
    print(acke)
    if acke is None or "OK" not in acke:  # Check if acknowledgment is valid
        print("Header error/ Wrong server error")  # Print an error message
        capt_img.close()  # Close the file
        return

    while True:
        b_value = button0.value()  # Get the button's current state
        packet = capt_img.read(512)  # Read the file in chunks of 512 bytes
        endof_file = False
        if not b_value:  # If the button is pressed
            dl_sdcard_comm.comm()  # Perform some SD card communication
            
        if not packet:
            print('End of file reached')  # Indicate the end of the file
            endof_file = True
            break

        if endof_file == False:
            print('Sending packet...')  # Indicate that a packet is being sent
            print(len(packet))  # Print the size of the packet
            bgsocket.sendBytes(packet)  # Send the packet over the socket

            time.sleep(0.1)  # Delay for stability
            toggle(led7.value())  # Toggle the LED state
            time.sleep(0.1)  # Delay for stability
            toggle(led7.value())  # Toggle the LED state again

    done = bgsocket.recv(10)  # Wait for a "DONE" message from the server
    donee = done[1]  # Extract the "DONE" message
    print(donee)
    if 'DONE' in donee:  # Check if the transfer was successful
        print("Obrázek úspěšně odeslán.")  # Print a success message
    else:
        print("Přenos selhal nebo neúplný.")  # Print a failure message
    capt_img.close()  # Close the file
