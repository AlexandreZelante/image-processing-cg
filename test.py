import cv2
import numpy as np
img1 = cv2.imread('./input/rg.jpg')
row,col,ch = img1.shape
g = [ ]  #the list in which we will stuff single grayscale pixel value inplace of 3 RBG values
#this function converts each RGB pixel value into single Grayscale pixel value and appends that value to list 'g'
def rgb2gray(Img):
  global g
  row,col,CHANNEL = Img.shape
  for i in range(row):
    for j in range(col):
      a = (Img[i,j,0]*0.07 + Img[i,j,1]*0.72 + Img[i,j,2] *0.21) #the algorithm i used id , G =  B*0.07 + G*0.72 + R* 0.21
      g.append(a)
rgb2gray(img1)  #convert the img1 into grayscale
gr = np.array(g)  #convert the list 'g' containing grayscale pixel values into numpy array
cv2.imwrite("test1.png" , gr.reshape(row,col)) #save the image file as test1.jpg