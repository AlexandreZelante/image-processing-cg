import cv2
import numpy
def convertToGrayScale(imageArray):
    grayImage = []
    imageHeight = len(imageArray)
    imageWidth = len(imageArray[0])

    for i in range(imageHeight):
        for j in range(imageWidth):
            grayImage.append(int(imageArray[i][j][0]*0.2126 + imageArray[i][j][1]*0.7152 + imageArray[i][j][2] * 0.0722)) 
    
    return grayImage

def applyAdaptiveThreshold():
    adaptiveThresholdImage = []
    img = cv2.imread('./input/rg.jpg',0)
    imageArray = numpy.asarray(img)
    img = cv.medianBlur(imageArray,5)
    
    # grayImage = convertToGrayScale(imageArray)

    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    return th3

applyAdaptiveThreshold()