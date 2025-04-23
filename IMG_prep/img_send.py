#import machine
import time
import usocket as socket

def toggle(led):
    if led == 1:
        led = 0
    else:
        led = 1
    return led

def send_img(led7, random_num):
    #addr = socket.getaddrinfo(server_ip, server_port)[0] #get the address of the server
    #sock.connect(addr) #connect to the server
    rootimg = '/sd/image' + str(random_num) + '.png'
    try:
        capt_img = open(rootimg, 'rb')
    except:
        capt_img = open(r'c:\ZCoding\IoT\CamTrap\IoT_CamTrap\codedev_win\IMG_prep\testpic.jpg', 'rb')
    #print(img)
    while True:
        packet = capt_img.read(512)
        endof_file = False
        if not packet:
            print('End of file reached') #send end of file packet for the receiver to know that the image is done sending
            endof_file = True
            #sock.close() #close the socket connection
            break

        if endof_file == False:
            print('Sending packet...') #send the image packet to the receiver
            #Packet sending commands 
            #sock.send(packet) #send the packet to the receiver
            time.sleep(0.1) #simulate the time taken to send the packet
            toggle(led7.value())
            time.sleep(0.1) #simulate the time taken to send the packet
            toggle(led7.value())
            print('Packet sent')
        
            
#TEST function call goofy aaah 
#send_img(1,1)