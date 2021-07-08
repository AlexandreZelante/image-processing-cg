import os
from PIL import Image, ImageOps
import numpy
import cv2

# Array Structure
# [
#   # Row
#   [
#     # Column
#     [R,G,B], [R,G,B], [R,G,B]
#   ]
# ]

INPUT_DIR = "./input/"
OUTPUT_DIR = "./output/"

def convertToGrayScale(imageArray):
  grayImage = []

  imageHeight = len(imageArray)
  imageWidth = len(imageArray[0])

  for i in range(imageHeight):
      for j in range(imageWidth):
          grayImage.append(int(imageArray[i][j][0]*0.2126 + imageArray[i][j][1]*0.7152 + imageArray[i][j][2] * 0.0722)) 

  return grayImage


def pipeline():
  for filename in os.listdir(INPUT_DIR):
    print(filename)
    im = Image.open(INPUT_DIR + filename) #1152 x 864

    imageArray = numpy.asarray(im)

    imageHeight = len(imageArray)
    imageWidth = len(imageArray[0])
    print("Numero de linhas: "+ str(len(imageArray))) #Linha 0, coluna 0
    print("Numero de colunas: "+ str(len(imageArray[0]))) #Linha 0, coluna 0
    
    # Step 1: Convert to Gray Scale
    grayImage = convertToGrayScale(imageArray)

    # Step 2: Adaptive Threshold
    

    # Save image
    cv2.imwrite(OUTPUT_DIR + "final_" + filename, numpy.array(grayImage).reshape(imageHeight,imageWidth))


pipeline()

