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
    row = []
    for j in range(imageWidth):
      row.append(int(imageArray[i][j][0]*0.2126 + imageArray[i][j][1]*0.7152 + imageArray[i][j][2] * 0.0722))
    grayImage.append(row)

  return grayImage

def applyAdaptiveThreshold(imageArray):
  adaptiveThresholdImage = []

  th3 = cv2.adaptiveThreshold(imageArray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  return th3


def applyAdaptiveThresholdTest(input_img, sub_thresh = 0.15):
  # input_img = cv2.imread('./input/rg.jpg')
  integralimage = cv2.integral(input_img, cv2.CV_32F)
#  https://stackoverflow.com/questions/16546130/efficient-implementation-of-summed-area-table-integral-image-in-r
  width = input_img.shape[1]
  print("width "+str(width))
  height = input_img.shape[0]
  print("height "+str(height))
  win_length = int(width / 10)
  image_thresh = numpy.zeros((height, width, 1), dtype = numpy.uint8)
#    perform threshholding
  for j in range(height):
      for i in range(width):
          x1 = i - win_length
          x2 = i + win_length
          y1 = j - win_length
          y2 = j + win_length

          #check the border
          if (x1 < 0):
              x1 = 0
          if (y1 < 0):
              y1 = 0
          if (x2 > width):
              x2 = width - 1
          if (y2 > height):
              y2 = height - 1
          count = (x2 - x1) * (y2 - y1)

          sum = integralimage[y2, x2] - integralimage[y1, x2] - integralimage[y2, x1] + integralimage[y1, x1]
          
          if (int)(input_img[j][i] * count) < (int) (sum * (1.0 - sub_thresh)):
              image_thresh[j, i] = 0
          else:
              image_thresh[j, i] = 255

  return image_thresh


def integralImage(grayImage):
  # create the array of integral image
  array_integral = numpy.zeros_like(grayImage)

  # compute values for integral image
  for r in range(imageHeight):
      for c in range(imageWidth):
          # compute the integral image (fast way)
          B = 0
          C = 0
          D = 0
          if r > 0:
              B = array_integral[r - 1, c]
          if c > 0:
              C = array_integral[r, c - 1]
          if r > 0 and c > 0:
              D = array_integral[r - 1, c - 1]

          array_integral[r, c] = grayImage[r, c] + B + C - D
          
  return array_integral
          # compute the integral image (slow way)
          # for i in range(r):
          #     for j in range(c):
          #         array_integral[r, c] = array_integral[r, c] + array_intensity[i, j]


def pipeline():
  for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
      print(filename)
      # im = Image.open(INPUT_DIR + filename) #1152 x 864
      image = cv2.imread(INPUT_DIR + filename) 

      # imageArray = numpy.asarray(img)

      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      global imageHeight
      imageHeight = len(image)

      global imageWidth
      imageWidth = len(image[0])

      # print("Numero de linhas: "+ str(len(imageArray)))
      # print("Numero de colunas: "+ str(len(imageArray[0])))
      
      # # Step 1: Convert to Gray Scale
      grayImage = convertToGrayScale(image)
      integral = integralImage(gray)
      cv2.imwrite(OUTPUT_DIR + "grayImage_" + filename, integral)

      # # Step 2: Adaptive Threshold
      # adaptiveThresholdImage = applyAdaptiveThresholdTest(numpy.array(grayImage))
      # cv2.imwrite(OUTPUT_DIR + "adaptiveThresholdImage_" + filename, numpy.array(adaptiveThresholdImage))
      # print("Imagem com o Threshold aplicado gerado")
      
      # Step 3: Deskew image (Alinhar)

      # Save image
      # cv2.imwrite(OUTPUT_DIR + "final_" + filename, numpy.array(grayImage).reshape(imageHeight,imageWidth))


pipeline()
# print(applyAdaptiveThresholdTest())
