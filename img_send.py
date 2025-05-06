import machine
import time
import BG77
import os
import dl_sdcard_comm



def toggle(led):
    if led == 1:
        led = 0
    else:
        led = 1
    return led

def send_img(bgsocket, led7, random_num):
    #conectos grandos to tcpos
   
    rootimg = '/image' + str(random_num) + '.png'
    try:
        capt_img = open('/sd/image4.png', 'rb')
    except:
        print('chyba otevření img4.png')
    filesize = os.stat(rootimg)[6]    
    header = f"SIMG {filesize}"
    #print(img)
    while True:
        packet = capt_img.read(512)
        endof_file = False
        if not packet:
            print('End of file reached') #send end of file packet for the receiver to know that the image is done sending
            endof_file = True
            break

        if endof_file == False:
            print('Sending packet...') #send the image packet to the receiver
            print(len(packet))
            #sending commands
            bgsocket.send(packet)

            time.sleep(0.1)
            toggle(led7.value())
            time.sleep(0.1)
            toggle(led7.value())
            
def send_imgv2(bgsocket, led7, random_num):
    rootimg = '/image' + str(random_num) + '.png'
    capt_img = open('/sd/image4.png', 'rb')
    filesize = os.stat(rootimg)[6]  # velikost souboru v bajtech

    # 1. Pošli hlavičku s velikostí souboru
    header = f"SIMG {filesize}\n"
    bgsocket.send(header)
    
    #Čekej na OK
    ack = bgsocket.recv(10)
    acke = ack[1]
    print(acke)
    if acke is None or "OK" not in acke:
        print("Header error/ Wrong server error")
        capt_img.close()
        return
    
    # 3. Pošli soubor po částech
    while True:
        packet = capt_img.read(512)
        endof_file = False
        if not packet:
            print('End of file reached') #send end of file packet for the receiver to know that the image is done sending
            endof_file = True
            break

        if endof_file == False:
            print('Sending packet...') #send the image packet to the receiver
            print(len(packet))
            #sending commands
            
            bgsocket.sendBytes(packet)

            time.sleep(0.1)
            toggle(led7.value())
            time.sleep(0.1)
            toggle(led7.value())

    # 4. Čekej na DONE
    done = bgsocket.recv(10)
    donee = done[1]
    print(donee)
    if 'DONE' in donee:
        print("Obrázek úspěšně odeslán.")
    else:
        print("Přenos selhal nebo neúplný.")
    capt_img.close()


#v3 - nereálná, snažení otevření dalšího socketu, když mám otevřený jiný.   
def send_imgv3(bgsocket, led7, random_num):
    button0 = machine.Pin(6, machine.Pin.IN)
    b_value = button0.value()
    
    rootimg = '/image' + str(random_num) + '.png'
    capt_img = open('/sd/image4.png', 'rb')
    filesize = os.stat(rootimg)[6]  # velikost souboru v bajtech

    # 1. Pošli hlavičku s velikostí souboru
    header = f"SIMG {filesize}\n"
    bgsocket.send(header)
    
    # 2. Čekej na OK
    ack = bgsocket.recv(10)
    acke = ack[1]
    print(ack)
    print(acke)
    if acke is None or "OK" not in acke:
        print("Header error/ Wrong server error")
        capt_img.close()
        return
    



    # 3. Pošli soubor po částech
    while True:
        b_value = button0.value()
        packet = capt_img.read(512)
        endof_file = False
        if not b_value:
            dl_sdcard_comm.comm()
            
        if not packet:
            print('End of file reached') #send end of file packet for the receiver to know that the image is done sending
            endof_file = True
            break

        if endof_file == False:
            print('Sending packet...') #send the image packet to the receiver
            print(len(packet))
            #sending commands
            
            bgsocket.sendBytes(packet)

            time.sleep(0.1)
            toggle(led7.value())
            time.sleep(0.1)
            toggle(led7.value())

    # 4. Čekej na DONE
    done = bgsocket.recv(10)
    donee = done[1]
    print(donee)
    if 'DONE' in donee:
        print("Obrázek úspěšně odeslán.")
    else:
        print("Přenos selhal nebo neúplný.")
    capt_img.close()    
      
        