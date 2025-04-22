import machine
import time
try:
    capt_img = open('testpic.jpg', 'rb')
except:
    capt_img = open(r'c:\ZCoding\IoT\CamTrap\IoT_CamTrap\codedev_win\IMG_prep\testpic.jpg', 'rb')
img = bytearray(capt_img.read())
print(img)

