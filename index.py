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

# Converte a imagem para escala de cinza
def convertToGrayScale(imageArray):
  grayImage = []
  for i in range(imageHeight):
    row = []
    for j in range(imageWidth):
      # Utilizando a percepção de cores para converter os pixeis para a escala de cinza
      row.append(int(imageArray[i][j][0]*0.2126 + imageArray[i][j][1]*0.7152 + imageArray[i][j][2] * 0.0722))
    grayImage.append(row)
  return grayImage

# Calcula a integral da imagem permitindo fazer a binarização em tempo linear
def getIntegralImage(input_img):
  integralImage = []
  for i in range(imageHeight):
    sum = 0
    row = []
    for j in range(imageWidth):
      sum = sum + input_img[i][j]
      if (i == 0):
         row.append(sum)
      else:
        row.append(integralImage[i-1][j]+sum)
    integralImage.append(row)  
  return integralImage

# Aplica binzarização com threshold adaptativo
def applyAdaptiveThresholdTest(input_img, integralimage, sub_thresh = 0.15):
  win_length = int(imageWidth / 10)
  threshImage = []
  for i in range(imageHeight):
      row = []
      for j in range(imageWidth):
          x1 = j - win_length
          x2 = j + win_length
          y1 = i - win_length
          y2 = i + win_length

          #check the border
          if (x1 < 0):
              x1 = 0
          if (y1 < 0):
              y1 = 0
          if (x2 >= imageWidth):
              x2 = imageWidth - 1
          if (y2 >= imageHeight):
              y2 = imageHeight - 1
          count = (x2 - x1) * (y2 - y1)

          sum = integralimage[y2][x2] - integralimage[y1][x2] - integralimage[y2][x1] + integralimage[y1][x1]
          
          if (int)(input_img[i][j] * count) < (int) (sum * (1.0 - sub_thresh)):
              row.append(0)
          else:
              row.append(255)
      threshImage.append(row)

  return threshImage

def pipeline():
  for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
      print(filename)
      image = cv2.imread(INPUT_DIR + filename) 

      # gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      global imageHeight
      imageHeight = len(image)

      global imageWidth
      imageWidth = len(image[0])

      print("Numero de colunas: "+ str(len(imageHeight)))
      print("Numero de linhas: "+ str(len(imageWidth)))
      
      # Step 1: Convert to Gray Scale
      grayImage = convertToGrayScale(image)
      cv2.imwrite(OUTPUT_DIR + "grayImage_" + filename, numpy.array(grayImage))
      print("Imagem Cinza gerada")
      
      # Artigo usado como base: http://people.scs.carleton.ca/~roth/iit-publications-iti/docs/gerh-50002.pdf
      # Step 2: Get Integral Image
      integralimage = getIntegralImage(grayImage)
      cv2.imwrite(OUTPUT_DIR + "integralImage_" + filename, numpy.array(integralimage))
      print("Imagem Integral gerada")

      # Step 3: Adaptive Threshold
      adaptiveThresholdImage = applyAdaptiveThresholdTest(grayImage, integralimage)
      cv2.imwrite(OUTPUT_DIR + "adaptiveThresholdImage_" + filename, numpy.array(adaptiveThresholdImage))
      print("Imagem com o Threshold aplicado gerada")
      
      # Step 3: Deskew image (Alinhar)

      # Save image
      # cv2.imwrite(OUTPUT_DIR + "final_" + filename, numpy.array(grayImage).reshape(imageHeight,imageWidth))


pipeline()



# def applyAdaptiveThreshold(imageArray):
#   adaptiveThresholdImage = []

#   th3 = cv2.adaptiveThreshold(imageArray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

#   return th3