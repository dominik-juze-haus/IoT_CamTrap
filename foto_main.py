import machine  # Importing the machine module for hardware interaction.
import time  # Importing the time module for delays and time tracking.
import BG77  # Importing the BG77 module for handling the BG77 modem.
import sdcard  # Importing the sdcard module for SD card operations.
import os  # Importing the os module for file system operations.
import random  # Importing the random module for generating random numbers.
import img_send  # Importing the img_send module for sending images.
import _thread  # Importing the _thread module for multithreading.
import dl_sdcard_comm  # Importing the dl_sdcard_comm module for SD card communication.

def monitor_radio(module, bgsocket, led_7, random_num):
    button0 = machine.Pin(6, machine.Pin.IN)  # Configuring button0 as an input pin.
    time.sleep(2)  # Delay to allow the system to stabilize.
    retry = 0  # Counter for retry attempts.
    i = 1  # Counter for retry intervals.
    while True:
        status = -1  # Initializing the socket status.
        module.sendCommand("AT+QCFG=\"iotopmode\",2,1\r\n")  # Configuring IoT operation mode.
        time.sleep(3)  # Delay for the command to take effect.
        bgsocket.connect("62.245.74.185", 26903)  # Connecting to the server.
        status = bgsocket.getStatus()  # Getting the socket status.
        print(status)  # Printing the socket status.

        if module.isRegistered() and status == 2:  # Checking if the module is registered and socket is ready.
            print("Síť i socket připraveny.")  # Network and socket are ready.
            time.sleep(3)  # Delay before sending the image.
            retry = 0  # Resetting the retry counter.
            img_send.send_imgv2(bgsocket, led_7, random_num)  # Sending the image.
            bgsocket.close()  # Closing the socket.
            return True  # Exiting the function with success.
        else:
            if retry >= 4:  # If retries exceed the limit.
                print(retry)  # Printing the retry count.
                print("Po hodině stále žádný signál.")  # No signal after an hour.
                print("Síť není připravena – ukládám pouze na SD.")  # Saving only to SD card.
                bgsocket.close()  # Closing the socket.
                retry = 0  # Resetting the retry counter.
                i = 0  # Resetting the interval counter.
                return False  # Exiting the function with failure.
            print(f"Není připojení – čekám {i}. 15 min.")  # Waiting for the next retry.
            retry += 1  # Incrementing the retry counter.
            i += 1  # Incrementing the interval counter.

        start = time.time()  # Recording the start time.
        while time.time() - start < 20:  # Looping for 20 seconds.
            b_value = button0.value()  # Reading the button0 value.
            if not b_value:  # If button0 is pressed.
                dl_sdcard_comm.comm()  # Perform SD card communication.
            time.sleep(0.5)  # Delay to avoid rapid polling.

# Initializing the SPI interface for the SD card.
spi_handler = machine.SPI(1, sck=10, mosi=11, miso=12, baudrate=1000000)
cs = machine.Pin(23, machine.Pin.OUT, value=1)  # Configuring the chip select pin for the SD card.
sd = sdcard.SDCard(spi_handler, cs)  # Initializing the SD card.
os.mount(sd, "/sd")  # Mounting the SD card to the file system.

led_7 = machine.Pin(7, machine.Pin.OUT)  # Configuring LED pin as output.
led_7.value(0)  # Turning off the LED.

button0 = machine.Pin(6, machine.Pin.IN)  # Configuring button0 as an input pin.
button1 = machine.Pin(28, machine.Pin.IN)  # Configuring button1 as an input pin.

# Initializing the UART interface for the BG77 module.
bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout=0, timeout_char=1)

bg_uart.write(bytes("AT\r\n", "ascii"))  # Sending an AT command to the BG77 module.
print(bg_uart.read(10))  # Reading the response from the BG77 module.

# Initializing the BG77 module.
module = BG77.BG77(bg_uart, verbose=True, radio=False)

time.sleep(3)  # Delay to allow the module to initialize.
module.sendCommand("AT+CFUN=1\r\n")  # Setting the module to full functionality.
time.sleep(2)  # Delay for the command to take effect.
test_sim = module.sendCommand("AT+CPIN?\r\n")  # Checking the SIM card status.

print(test_sim)  # Printing the SIM card status.
while "+CME ERROR" in test_sim:  # If there is an error with the SIM card.
    print("Chyba SIM – restartuji modul...")  # SIM card error, restarting the module.
    module.sendCommand("AT+CFUN=0\r\n")  # Setting the module to minimum functionality.
    time.sleep(10)  # Delay before restarting.
    module.sendCommand("AT+CFUN=1\r\n")  # Restarting the module.
    time.sleep(3)  # Delay for the module to initialize.
    test_sim = module.sendCommand("AT+CPIN?\r\n")  # Checking the SIM card status again.

# Configuring the module for specific bands and IoT operation.
module.sendCommand("AT+QCFG=\"band\",0x0,0x80084,0x80084,1\r\n")
module.setRadio(1)  # Enabling the radio.
module.setAPN("lpwa.vodafone.iot")  # Setting the APN for the network.

module.sendCommand("AT+CEREG?\r\n")  # Checking the network registration status.
module.sendCommand("AT+CMEE=2\r\n")  # Enabling detailed error reporting.
module.sendCommand("AT+QCFG=\"iotopmode\",1,1\r\n")  # Configuring IoT operation mode.

module.setOperator(1, "23003")  # Setting the network operator.
module.sendCommand("AT+QNWINFO\r\n")  # Getting network information.
result, bgsocket = module.socket(BG77.AF_INET, BG77.SOCK_STREAM)  # Creating a socket.
if not result:  # If socket creation fails.
    openingFailedDoSomethingAboutIt()  # Handle the failure.
bgsocket.settimeout(5)  # Setting the socket timeout.
print("Připraveno k použivání")  # Ready for use.

# Infinite loop for handling button presses and operations.
while True:
    b_value = button0.value()  # Reading the button0 value.
    bb_value = button1.value()  # Reading the button1 value.
    if not bb_value:  # If button1 is pressed.
        print(os.listdir("/sd"))  # Listing the files on the SD card.
        img = "image4.png"  # File to be removed.
        if img in os.listdir("/sd"):  # If the file exists.
            os.remove("/sd/" + img)  # Removing the file.
            print("image4.png byl odstraněn.")  # File removed.
            print(os.listdir("/sd"))  # Listing the files again.
        else:
            print("image4.png nebyl nalezen")  # File not found.
    if not b_value:  # If button0 is pressed.
        # Sending various AT commands to the module.
        module.sendCommand("AT+QCFG=\"iotopmode\",1,1\r\n")
        module.sendCommand("AT+QIRD=1\r\n")
        module.sendCommand("AT+QCSCON=1\r\n")
        module.sendCommand("AT+QIOPEN=1,1,\"UDP\",\"147.229.148.105\",7004\r\n")
        module.sendCommand("AT+QISEND=1,15\r\n")
        module.sendCommand("fotka zachycena\r\n")
        module.sendCommand("AT+QIRD=1\r\n")
        module.sendCommand("AT+QICLOSE=1\r\n")

        random_num = random.randint(1, 3)  # Generating a random number.
        imgstring = "/sd/image4.png"  # Path for the new image.

        file = open(imgstring, "wb")  # Opening the file for writing.
        with open(f"image{random_num}.png", "rb") as f:  # Opening a random image for reading.
            while True:
                byte = f.read(1)  # Reading one byte at a time.
                if not byte:  # If end of file is reached.
                    break
                file.write(byte)  # Writing the byte to the new file.
        file.close()  # Closing the file.
        print(f"uložil se obrázek s číslem {random_num}\r\n")  # Image saved.
        print(os.listdir("/sd"))  # Listing the files on the SD card.

        monitor_radio(module, bgsocket, led_7, random_num)  # Monitoring the radio and sending the image.

        print("Připraveno k použivání")  # Ready for use.
    else:
        led_7.value(1)  # Turning on the LED.

    time.sleep(1)  # Delay to avoid rapid polling.
