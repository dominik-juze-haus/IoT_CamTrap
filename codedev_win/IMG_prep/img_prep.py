import os
try:
    import ulab.numpy as np
except ImportError:
    import numpy as np


def resize_image(image):
    # Convert the byte array to a numpy array
    image_array = np.frombuffer(image, dtype=np.uint8)
    print(f"Image array shape: {image_array}")
    # Reshape the array to a 2D image (assuming grayscale for simplicity)
    height = image_array.size // 640  # Assuming a fixed width of 640 pixels
    width = image_array.size // height
    image_2d = image_array.reshape((height, width))

    # Resize the image to a quarter of its original size
    new_height = height // 4
    new_width = width // 4
    resized_image = np.resize(image_2d, (new_height, new_width))

    # Convert the resized image back to a byte array
    resized_image_bytes = resized_image.tobytes()

    return resized_image_bytes


img_path = open(r'c:\ZCoding\IoT\CamTrap\IoT_CamTrap\codedev_win\IMG_prep\testpic.jpg', 'rb')
img_fullsize = bytearray(img_path.read())
print(img_fullsize)
img_compressed = resize_image(img_fullsize) # Resize to quarter size




