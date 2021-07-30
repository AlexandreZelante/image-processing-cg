import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import xlsxwriter
# image = cv.imread('./input/RGCortado.jpg')
image = cv.imread('./input/RGCortado.jpg')
workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()


# Normal threshold
# ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
# ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
# ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
# ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
# titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
# for i in range(6):
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])

# plt.show()

# Adaptive
# img = cv.imread('./input/rg.jpg',0)
# img = cv.medianBlur(img,5)
# ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
#             cv.THRESH_BINARY,11,2)
# th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv.THRESH_BINARY,11,2)
# titles = ['Original Image', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

def getIntegralAt(integral, width, x1, y1, x2, y2): 
    result = integral[x2 + y2 * width]
    if (y1 > 0):
        result -= integral[x2 + (y1 - 1) * width]
        if (x1 > 0):
            result += integral[(x1 - 1) + (y1 - 1) * width]
        
    
    if (x1 > 0):
        result -= integral[(x1 - 1) + (y2) * width];
    
    return result;

def adaptiveThreshold(sub_thresh = 0.15):
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
#    Calculating integral image
    # integralimage = np.zeros_like(gray_image, dtype=np.uint32)
    integralimage = cv.integral(gray_image, cv.CV_32F)
    
    width = gray_image.shape[1]
    print("width "+str(width))
    height = gray_image.shape[0]
    print("height "+str(height))
    win_length = int(width / 10)
    image_thresh = np.zeros((height, width, 1), dtype = np.uint8)
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
            worksheet.write(j, i, sum)
            
            if (int)(gray_image[j, i] * count) < (int) (sum * (1.0 - sub_thresh)):
                image_thresh[j, i] = 0
            else:
                image_thresh[j, i] = 255

    return image_thresh

# def thresholdIntegral(T = 0.15):
# #   outputMat=np.uint8(np.ones(inputMat.shape)*255)
#   s = cv.integral(image)

#   outputMat=np.zeros(image.shape)
#   nRows = image.shape[0]
#   nCols = image.shape[1]
#   S = int(max(nRows, nCols) / 8)

#   s2 = int(S / 4)

#   for i in range(nRows):
#       y1 = i - s2
#       y2 = i + s2

#       if (y1 < 0) :
#           y1 = 0
#       if (y2 >= nRows):
#           y2 = nRows - 1

#       for j in range(nCols):
#           x1 = j - s2
#           x2 = j + s2

#           if (x1 < 0) :
#               x1 = 0
#           if (x2 >= nCols):
#               x2 = nCols - 1
#           count = (x2 - x1)*(y2 - y1)

#           sum=s[y2][x2]-s[y2][x1]-s[y1][x2]+s[y1][x1]

#           if ((int)(image[i][j] * count) < (int)(sum * (1.0 - T))):
#               outputMat[i][j] = 255
#           else:
#               outputMat[j][i] = 0

#   return outputMat

imageNice = adaptiveThreshold()
cv.imwrite("final_fodase.jpg", np.array(imageNice))
plt.subplot(2,2,1),plt.imshow(imageNice,'gray')
plt.xticks([]),plt.yticks([])
plt.show()
workbook.close()

# void thresholdIntegral(cv::Mat &inputMat, cv::Mat &outputMat)
# {
#     // accept only char type matrices
#     CV_Assert(!inputMat.empty());
#     CV_Assert(inputMat.depth() == CV_8U);
#     CV_Assert(inputMat.channels() == 1);
#     CV_Assert(!outputMat.empty());
#     CV_Assert(outputMat.depth() == CV_8U);
#     CV_Assert(outputMat.channels() == 1);

#     // rows -> height -> y
#     int nRows = inputMat.rows;
#     // cols -> width -> x
#     int nCols = inputMat.cols;

#     // create the integral image
#     cv::Mat sumMat;
#     cv::integral(inputMat, sumMat);

#     CV_Assert(sumMat.depth() == CV_32S);
#     CV_Assert(sizeof(int) == 4);

#     int S = MAX(nRows, nCols)/8;
#     double T = 0.15;

#     // perform thresholding
#     int s2 = S/2;
#     int x1, y1, x2, y2, count, sum;

#     // CV_Assert(sizeof(int) == 4);
#     int *p_y1, *p_y2;
#     uchar *p_inputMat, *p_outputMat;

#     for( int i = 0; i < nRows; ++i)
#     {
#         y1 = i-s2;
#         y2 = i+s2;

#         if (y1 < 0){
#             y1 = 0;
#         }
#         if (y2 >= nRows) {
#             y2 = nRows-1;
#         }

#         p_y1 = sumMat.ptr<int>(y1);
#         p_y2 = sumMat.ptr<int>(y2);
#         p_inputMat = inputMat.ptr<uchar>(i);
#         p_outputMat = outputMat.ptr<uchar>(i);

#         for ( int j = 0; j < nCols; ++j)
#         {
#             // set the SxS region
#             x1 = j-s2;
#             x2 = j+s2;

#             if (x1 < 0) {
#                 x1 = 0;
#             }
#             if (x2 >= nCols) {
#                 x2 = nCols-1;
#             }

#             count = (x2-x1)*(y2-y1);

#             // I(x,y)=s(x2,y2)-s(x1,y2)-s(x2,y1)+s(x1,x1)
#             sum = p_y2[x2] - p_y1[x2] - p_y2[x1] + p_y1[x1];

#             if ((int)(p_inputMat[j] * count) < (int)(sum*(1.0-T)))
#                 p_outputMat[j] = 255;
#             else
#                 p_outputMat[j] = 0;
#         }
#     }
# }