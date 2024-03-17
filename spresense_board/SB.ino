/*
 *  camera.ino - Simple camera example sketch
 *  Copyright 2018, 2022 Sony Semiconductor Solutions Corporation
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 *  This is a test app for the camera library.
 *  This library can only be used on the Spresense with the FCBGA chip package.
 */

#include <SDHCI.h>
#include <stdio.h>  /* for sprintf */

#include <Camera.h>

#define BAUDRATE                (115200)
#define TOTAL_PICTURE_COUNT     (1)



// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;  // the number of the pushbutton pin
const int ledPin = 13;    // the number of the LED pin

SDClass  theSD;
int take_picture_count = 0;
File file;

String direction = "checkin";

// int buttonPin = 0;

/**
 * Print error message
 */

void printError(enum CamErr err)
{
  Serial.print("Error: ");
  switch (err)
    {
      case CAM_ERR_NO_DEVICE:
        Serial.println("No Device");
        break;
      case CAM_ERR_ILLEGAL_DEVERR:
        Serial.println("Illegal device error");
        break;
      case CAM_ERR_ALREADY_INITIALIZED:
        Serial.println("Already initialized");
        break;
      case CAM_ERR_NOT_INITIALIZED:
        Serial.println("Not initialized");
        break;
      case CAM_ERR_NOT_STILL_INITIALIZED:
        Serial.println("Still picture not initialized");
        break;
      case CAM_ERR_CANT_CREATE_THREAD:
        Serial.println("Failed to create thread");
        break;
      case CAM_ERR_INVALID_PARAM:
        Serial.println("Invalid parameter");
        break;
      case CAM_ERR_NO_MEMORY:
        Serial.println("No memory");
        break;
      case CAM_ERR_USR_INUSED:
        Serial.println("Buffer already in use");
        break;
      case CAM_ERR_NOT_PERMITTED:
        Serial.println("Operation not permitted");
        break;
      default:
        break;
    }
}

/**
 * Callback from Camera library when video frame is captured.
 */

void CamCB(CamImage img)
{

  /* Check the img instance is available or not. */

  if (img.isAvailable())
    {

      /* If you want RGB565 data, convert image data format to RGB565 */

      img.convertPixFormat(CAM_IMAGE_PIX_FMT_RGB565);

      /* You can use image data directly by using getImgSize() and getImgBuff().
       * for displaying image to a display, etc. */

      // Serial.print("Image data size = ");
      // Serial.print(img.getImgSize(), DEC);
      // Serial.print(" , ");

      // Serial.print("buff addr = ");
      // Serial.print((unsigned long)img.getImgBuff(), HEX);
      // Serial.println("");
    }
  else
    {
      Serial.println("Failed to get video stream image");
    }
}

/**
 * @brief Initialize camera
 */
void setup()
{
  CamErr err;

  // pinMode(PIN_D01, INPUT);
  Serial.println("started");

  // initialize the LED pin as an output:
  pinMode(LED0, OUTPUT);
  pinMode(LED1, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(digitalPinToPort(PIN_D22), INPUT);
  pinMode(digitalPinToPort(PIN_D23), INPUT);

  digitalWrite(LED0, LOW);
  digitalWrite(LED1, LOW);

  /* Open serial communications and wait for port to open */

  Serial.begin(BAUDRATE);
  while (!Serial)
    {
      ; /* wait for serial port to connect. Needed for native USB port only */
    }

  /* Initialize SD */
  while (!theSD.begin()) 
    {
      /* wait until SD card is mounted. */
      Serial.println("Insert SD card.");
    }

  /* begin() without parameters means that
   * number of buffers = 1, 30FPS, QVGA, YUV 4:2:2 format */

  Serial.println("Prepare camera");
  err = theCamera.begin();
  if (err != CAM_ERR_SUCCESS)
    {
      printError(err);
    }

  /* Start video stream.
   * If received video stream data from camera device,
   *  camera library call CamCB.
   */

  Serial.println("Start streaming");
  err = theCamera.startStreaming(true, CamCB);
  if (err != CAM_ERR_SUCCESS)
    {
      printError(err);
    }

  /* Auto white balance configuration */

  Serial.println("Set Auto white balance parameter");
  err = theCamera.setAutoWhiteBalanceMode(CAM_WHITE_BALANCE_DAYLIGHT);
  if (err != CAM_ERR_SUCCESS)
    {
      printError(err);
    }
 
  /* Set parameters about still picture.
   * In the following case, QUADVGA and JPEG.
   */

  Serial.println("Set still picture format");
  err = theCamera.setStillPictureImageFormat(
     CAM_IMGSIZE_QUADVGA_H,
     CAM_IMGSIZE_QUADVGA_V,
     CAM_IMAGE_PIX_FMT_JPG);
  if (err != CAM_ERR_SUCCESS)
    {
      printError(err);
    }
}

/**
 * @brief Take picture with format JPEG per second
 */
uint8_t val = 1;
void loop()
{

  /* Set pin to input mode */
  pinMode(PIN_D22, INPUT);
  pinMode(PIN_D23, INPUT);

  volatile uint8_t *port = portInputRegister(digitalPinToPort(PIN_D22));
  volatile uint8_t *mode = portModeRegister(digitalPinToPort(PIN_D22));

  volatile uint8_t *portout = portInputRegister(digitalPinToPort(PIN_D23));
  volatile uint8_t *modeout = portModeRegister(digitalPinToPort(PIN_D23));

  *mode = 1; /* Input setting */
  *modeout = 1;

  uint8_t val = *port; /* Read */
  if (val & 1){
    direction = "checkin";
    digitalWrite(LED0, HIGH);
  }

  uint8_t val2 = *portout; /* Read */
  if (val2 & 1){
    direction = "checkout";
    digitalWrite(LED1, HIGH);
  }

  sleep(0.1); /* wait for one second to take still picture. */

  // /* Set pin to input mode */
  // pinMode(PIN_D22, INPUT);

  // volatile uint8_t *port = portInputRegister(digitalPinToPort(PIN_D22));
  // volatile uint8_t *mode = portModeRegister(digitalPinToPort(PIN_D22));

  // *mode = 1; /* Input setting */

  // uint8_t val = *port; /* Read */
  // if (val & 1)
  //   Serial.println("High");
  // else
  //   Serial.println("Low");

  /* You can change the format of still picture at here also, if you want. */

  /* theCamera.setStillPictureImageFormat(
   *   CAM_IMGSIZE_HD_H,
   *   CAM_IMGSIZE_HD_V,
   *   CAM_IMAGE_PIX_FMT_JPG);
   */

  /* This sample code can take pictures in every one second from starting. */
  if ((val || val2) & 1)
    {
      val = 0;
  
      Serial.println("call takePicture()");
      CamImage img = theCamera.takePicture();


      if (img.isAvailable())
        {    
          char filename[16] = {0};
          sprintf(filename, "TEMP.jpg", take_picture_count);
    
          Serial.print("Save taken picture as ");
          Serial.print("TEMP.jpg");

          theSD.remove("TEMP.jpg");
          File myFile = theSD.open("TEMP.jpg", FILE_WRITE);
          myFile.write(img.getImgBuff(), img.getImgSize());
          myFile.close();

          file = theSD.open("TEMP.jpg");
          if (!file) {
            Serial.println("Could not open file for reading");
            return;
          }

          Serial.println("");

          // Read the file and send it over serial
          size_t fileSize = file.size();
          Serial.println(fileSize);
          
          // send if chilent is cheking in our checking out
          Serial.println(direction);

           // Read and send image data in 1024-byte chunks
          uint8_t chunk[1024];
          size_t bytesRead = 0;
          while (bytesRead < fileSize) {
            size_t bytesToRead = min(sizeof(chunk), fileSize - bytesRead);
            size_t bytesReadThisRound = file.read(chunk, bytesToRead);
            Serial.write(chunk, bytesReadThisRound);
            bytesRead += bytesReadThisRound;
            file.seek(bytesRead); // Move the file pointer to the next chunk
          }

          file.close();
        }
      else
        {
          Serial.println("Failed to take picture");
        }

      digitalWrite(LED0, LOW);
      digitalWrite(LED1, LOW);

      // Serial.println("End.");
      // theCamera.end();
    }
  
}
