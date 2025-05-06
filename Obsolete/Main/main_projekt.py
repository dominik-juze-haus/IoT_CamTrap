import machine
import time
import BG77
import sdcard
import os
import random
import img_send


spi_handler = machine.SPI(1,sck=10, mosi= 11, miso = 12, baudrate = 1000000)
cs = machine.Pin(23, machine.Pin.OUT, value=1)
sd = sdcard.SDCard(spi_handler, cs)
os.mount(sd, "/sd")


#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#addr = socket.getaddrinfo('0.0.0.0', 7005)[0][-1]
#os.remove("/sd/image4.png")
#Setup peripherals
led_7 = machine.Pin(7, machine.Pin.OUT)
led_7.value(0)

button0 = machine.Pin(6, machine.Pin.IN)

bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout = 0, timeout_char=1)

bg_uart.write(bytes("AT\r\n","ascii"))
print(bg_uart.read(10))


module = BG77.BG77(bg_uart, verbose=True, radio=False)

time.sleep(3)
module.sendCommand("AT+CPIN?\r\n")
module.sendCommand("AT+CFUN=1\r\n")
module.sendCommand("AT+QCFG=\"band\",0x0,0x80084,0x80084,1\r\n")
module.setRadio(1)
module.setAPN("lpwa.vodafone.iot")

module.sendCommand("AT+CEREG?\r\n")
module.sendCommand("AT+QCFG=\"iotopmode\",1,1\r\n")

module.setOperator(1,"23003")
module.sendCommand("AT+QNWINFO\r\n")
if not module.isRegistered():
    makeSureModuleIsRegisteredBeforeOpeningSocket()
result, bgsocket = module.socket(BG77.AF_INET, BG77.SOCK_STREAM)
if not result:
    openingFailedDoSomethingAboutIt()
bgsocket.settimeout(5)
#Infinite Loop
while True:
    b_value = button0.value()
   
    if not b_value:
        module.sendCommand("AT+QIRD=1\r\n")
        module.sendCommand("AT+QCSCON=1\r\n")
        module.sendCommand("AT+QIOPEN=1,1,\"UDP\",\"147.229.148.105\",7004\r\n")
        module.sendCommand("AT+QISEND=1,15\r\n")
        module.sendCommand("fotka zachycena\r\n")
        module.sendCommand("AT+QIRD=1\r\n")
       
       
        #shutil.copy("/sd/image.png","/sd/image2.png")
        random_num = random.randint(1,3)
        imgstring = "/sd/image" + str(4) + ".png"
        #file = open("/sd/image4.png", "wb")
        file = open(imgstring, "wb")
        with open(f"image{random_num}.png", "rb") as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break
                file.write(byte)
        file.close()
        print(f"uložil se obrázek s číslem {random_num}\r\n" )
        print(os.listdir("/sd"))
       
        bgsocket.connect("0.0.0.0",7005)
        if module.isRegistered():    
            img_send.send_img(bgsocket ,led_7, random_num)
        bgsocket.close()
    else:
        led_7.value(0)
   
    #send_img() dodelat
    time.sleep(1)