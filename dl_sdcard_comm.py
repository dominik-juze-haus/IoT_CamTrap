import machine
import time
import BG77
import sdcard
import os
import random
import img_send
import nbLib
import uploadLib
import _thread






def comm():
    
    button0 = machine.Pin(6, machine.Pin.IN)
    b_value = button0.value()
    bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout = 0, timeout_char=1)
    bg_uart.write(bytes("AT\r\n","ascii"))
    print(bg_uart.read(10))
    module = BG77.BG77(bg_uart, verbose=True, radio=False) 
    
    module.sendCommand("AT+QCFG=\"iotopmode\",1,1\r\n")
    module.sendCommand("AT+QIRD=1\r\n")
    module.sendCommand("AT+QCSCON=1\r\n")
    module.sendCommand("AT+QIOPEN=1,1,\"UDP\",\"147.229.148.105\",7004\r\n")
    module.sendCommand("AT+QISEND=1,15\r\n")
    module.sendCommand("fotka zachycena\r\n")
    module.sendCommand("AT+QIRD=1\r\n")
    module.sendCommand("AT+QICLOSE=1\r\n")
   
   
 
    random_num = random.randint(1,3)
    imgstring = "/sd/image" + str(4) + ".png"
    
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
    return random_num