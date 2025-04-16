import machine
import time

capt_img = open('testpic.jpg', 'rb')
img = bytearray(capt_img.read())
print(img)

