import machine
import time
import BG77
import sdcard
import os
import random
import img_send
import _thread
import dl_sdcard_comm

def monitor_radio(module, bgsocket, led_7, random_num):
    button0 = machine.Pin(6, machine.Pin.IN)
    #62.245.74.185
    time.sleep(2)
    retry = 0
    i = 1
    while True:
        status = -1
        module.sendCommand("AT+QCFG=\"iotopmode\",2,1\r\n")
        time.sleep(3)
        bgsocket.connect("62.245.74.185", 26903)
        status = bgsocket.getStatus()
        print(status)
           

        if module.isRegistered() and status == 2:
            print("Síť i socket připraveny.")
            time.sleep(3)
            retry = 0 
            img_send.send_imgv2(bgsocket, led_7, random_num)
            bgsocket.close()
            return True
        else:            
            if retry >= 4:
                print(retry)
                print("Po hodině stále žádný signál.")
                print("Síť není připravena – ukládám pouze na SD.")
                bgsocket.close()
                retry = 0
                i = 0
                return False
            print(f"Není připojení – čekám {i}. 15 min.")
            retry += 1
            i += 1
            
        start = time.time()
        while time.time() - start < 20:
            b_value = button0.value()
            if not b_value:
                dl_sdcard_comm.comm()
            time.sleep(0.5)
        

spi_handler = machine.SPI(1,sck=10, mosi= 11, miso = 12, baudrate = 1000000)
cs = machine.Pin(23, machine.Pin.OUT, value=1)
sd = sdcard.SDCard(spi_handler, cs)
os.mount(sd, "/sd")


led_7 = machine.Pin(7, machine.Pin.OUT)
led_7.value(0)

button0 = machine.Pin(6, machine.Pin.IN)
button1 = machine.Pin(28, machine.Pin.IN)

bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout = 0, timeout_char=1)

bg_uart.write(bytes("AT\r\n","ascii"))
print(bg_uart.read(10))


module = BG77.BG77(bg_uart, verbose=True, radio=False)

time.sleep(3)
module.sendCommand("AT+CFUN=1\r\n")  
time.sleep(2)
test_sim = module.sendCommand("AT+CPIN?\r\n")

print(test_sim)
while "+CME ERROR" in test_sim:
    print("Chyba SIM – restartuji modul...")
    module.sendCommand("AT+CFUN=0\r\n") 
    time.sleep(10)
    module.sendCommand("AT+CFUN=1\r\n")  
    time.sleep(3)
    test_sim = module.sendCommand("AT+CPIN?\r\n")
module.sendCommand("AT+QCFG=\"band\",0x0,0x80084,0x80084,1\r\n")
module.setRadio(1)
module.setAPN("lpwa.vodafone.iot")

module.sendCommand("AT+CEREG?\r\n")
module.sendCommand("AT+CMEE=2\r\n")
module.sendCommand("AT+QCFG=\"iotopmode\",1,1\r\n")

module.setOperator(1,"23003")
module.sendCommand("AT+QNWINFO\r\n")
result, bgsocket = module.socket(BG77.AF_INET, BG77.SOCK_STREAM)
if not result:
    openingFailedDoSomethingAboutIt()
bgsocket.settimeout(5)
print("Připraveno k použivání")
#Infinite Loop
while True:
    b_value = button0.value()
    bb_value = button1.value()
    if not bb_value:
        
        print(os.listdir("/sd"))
        img = "image4.png"
        if img in os.listdir("/sd"):
            os.remove("/sd/" + img)
            print("image4.png byl odstraněn.")
            print(os.listdir("/sd"))
        else:
            print("image4.png nebyl nalezen")    
    if not b_value:
        #random_num = dl_sdcard_comm.comm()
        module.sendCommand("AT+QCFG=\"iotopmode\",1,1\r\n")
        module.sendCommand("AT+QIRD=1\r\n")
        module.sendCommand("AT+QCSCON=1\r\n")
        module.sendCommand("AT+QIOPEN=1,1,\"UDP\",\"147.229.148.105\",7004\r\n")
        module.sendCommand("AT+QISEND=1,15\r\n")
        module.sendCommand("fotka zachycena\r\n")
        module.sendCommand("AT+QIRD=1\r\n")
        module.sendCommand("AT+QICLOSE=1\r\n")
       
       
     
        random_num = random.randint(1,3)
        imgstring = "/sd/image4.png"
        
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
        
        monitor_radio(module, bgsocket, led_7, random_num)
        
        print("Připraveno k použivání")
          
    else:
        led_7.value(1)
   
    time.sleep(1)