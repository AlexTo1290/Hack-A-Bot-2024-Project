import serial
from PIL import Image
import io
import base64
import requests
import numpy as np
import json


LABELS = ["File", "Hammer", "Power Drill","Scissors", "Screwdriver"]

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

def classifyImage():
     with open("received_image.jpg", "rb") as image_file:
        # reduce image to 180 x 180
        image = Image.open(image_file)

        image = np.array(image)
        image = image / 255.0
        image = np.expand_dims(image, axis=0)  # Add an extra dimension

        exInput = image.tolist()

        data = json.dumps({"signature_name": "serving_default", "inputs":
                        {"input_1": exInput}
                        })
        headers = {"content-type": "application/json"}
        url = "http://localhost:8501/v1/models/model:predict"
        json_response = requests.post(url=url, data=data, headers=headers)
        print(json_response.text)
        # get index with largest number
        result = json.loads(json_response.text)
        highest = max(result['outputs'][0])
        index = result['outputs'][0].index(highest)
        print("Prediction:", LABELS[index])
        return LABELS[index]



def post_to_database(direc):
    with open("received_image.jpg", "rb") as image_file:
        image = Image.open(image_file)
        image = image.resize((180, 180))
        # numpy array
        image = image.convert('RGB')
        image.save("received_image.jpg")

    top_label = classifyImage()

    with open("received_image.jpg", "rb") as image_file:
        # reduce image to 180 x 180
        image_data = image_file.read()
        url = 'http://localhost:3000/checkIn/'+top_label
        if direc == b'checkout':
            url = "http://localhost:3000/checkOut/"+top_label
        response = requests.post(url, data=image_data, headers={'Content-Type': 'image/jpeg', 'label': top_label})
        if response.status_code == 200:
            print("Image sent to database")
        else:
            print("Error sending image to database")


# Wait until receiving the image size line
while True:  
    temp = str
    str = ser.readline().strip()
    if temp == str or str == b'':
        continue
    if str.isdigit():
        image_size = int(str)
        print("Image size:", image_size)
        direc =  ser.readline().strip()
        print("direction:", direc)
        readImage(image_size)      
        post_to_database(direc)
    else:
        print(str)
