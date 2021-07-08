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

imageHeight = 0
imageWidth = 0

def convertToGrayScale(imageArray):
  grayImage = []
  
  for i in range(imageHeight):
      for j in range(imageWidth):
          grayImage.append(int(imageArray[i][j][0]*0.2126 + imageArray[i][j][1]*0.7152 + imageArray[i][j][2] * 0.0722)) 

  return grayImage

def applyAdaptiveThreshold(imageArray):
  adaptiveThresholdImage = []

  th3 = cv2.adaptiveThreshold(imageArray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  return th3

def applyAdaptiveThresholdTest():
  # input_img = cv2.imread('./input/rg.jpg')

  # h = input_img.shape[0]
  # w = input_img.shape[1]

  # S = w/8
  # s2 = S/2
  # T = 15.0

  # # print(h)

  # #integral img
  # int_img = numpy.zeros_like(input_img, dtype=numpy.uint32)
  # print(int_img)
  # for col in range(w):
  #   for row in range(h):
  #     # print('row')
  #     int_img[row,col] = input_img[0:row,0:col].sum()
  #output img
  # out_img = numpy.zeros_like(input_img)    

  # for col in range(w):
  #     for row in range(h):
  #         #SxS region
  #         y0 = max(row-s2, 0)
  #         y1 = min(row+s2, h-1)
  #         x0 = max(col-s2, 0)
  #         x1 = min(col+s2, w-1)

  #         count = (y1-y0)*(x1-x0)

  #         sum_ = int_img[y1, x1]-int_img[y0, x1]-int_img[y1, x0]+int_img[y0, x0]

  #         if input_img[row, col]*count < sum_*(100.-T)/100.:
  #             out_img[row,col] = 0
  #         else:
  #             out_img[row,col] = 255

  # return out_img


def pipeline():
  for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
      print(filename)
      im = Image.open(INPUT_DIR + filename) #1152 x 864

      imageArray = numpy.asarray(im)

      global imageHeight
      imageHeight = len(imageArray)

      global imageWidth
      imageWidth = len(imageArray[0])
      print("Numero de linhas: "+ str(len(imageArray)))
      print("Numero de colunas: "+ str(len(imageArray[0])))
      
      # Step 1: Convert to Gray Scale
      grayImage = convertToGrayScale(imageArray)
      cv2.imwrite(OUTPUT_DIR + "grayImage_" + filename, numpy.array(grayImage).reshape(imageHeight,imageWidth))
      print("Imagem em escala de cinza gerada")

      # Step 2: Adaptive Threshold
      adaptiveThresholdImage = applyAdaptiveThresholdTest(imageArray)
      cv2.imwrite(OUTPUT_DIR + "adaptiveThresholdImage_" + filename, numpy.array(adaptiveThresholdImage).reshape(imageHeight,imageWidth))
      print("Imagem com o Threshold aplicado gerado")
      

      # Save image
      cv2.imwrite(OUTPUT_DIR + "final_" + filename, numpy.array(grayImage).reshape(imageHeight,imageWidth))


pipeline()
# print(applyAdaptiveThresholdTest())
