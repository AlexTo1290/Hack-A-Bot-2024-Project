import serial
from PIL import Image
import io

# Configure the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

str = ""

def readImage(image_size):
    # Open a file to write the image data
    with open("received_image.jpg", "wb") as f:
        # Read image data in chunks and write it to the file
        bytes_read = 0
        
        print("Receiving image data...")
        while bytes_read < image_size:
            chunk = ser.read(min(1024, image_size - bytes_read))  # Read in chunks
            f.write(chunk)
            bytes_read += len(chunk)
            # print("Bytes read:", bytes_read)
        print("Image data received.")



# Wait until receiving the image size line
while True:  
    temp = str
    str = ser.readline().strip()
    if temp == str or str == b'':
        continue
    if str.isdigit():
        image_size = int(str)
        print("Image size:", image_size)
        print("direction:", ser.readline().strip())
        readImage(image_size)
    else:
        print(str)
