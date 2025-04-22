#import machine
import time

def toggle(led):
    if led == 1:
        led = 0
    else:
        led = 1
    return led

def send_img(server_ip, server_port, led7):

    try:
        capt_img = open('testpic.jpg', 'rb')
    except:
        capt_img = open(r'c:\ZCoding\IoT\CamTrap\IoT_CamTrap\codedev_win\IMG_prep\testpic.jpg', 'rb')
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
            #toggle(led7.value())
            #toggle(led7.value())
            ack = b'ACK' # Simulate receiving an ACK

        #print(packet)
        if ack != b'ACK':
            print('No ACK received, retrying...')
            time.sleep(1)
            packet.seek(packet.tell() - 512)
            
#TEST function call goofy aaah 
#send_img(1,1,1)
