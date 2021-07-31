import os
import numpy
import cv2
import pytesseract
import math
import json
import re
import copy
# Apenas para mostrar as imagens no colab
from IPython.display import Image, display

# Estrutura do array
# [
#   # Linha
#   [
#     # Coluna
#     [R,G,B], [R,G,B], [R,G,B]
#   ]
# ]

INPUT_DIR = "./input/"
OUTPUT_DIR = "./output/"

imageHeight = 0
imageWidth = 0

# Pontos em porcentagem de corte da imagem
# Com o seguinte padrão: [startHeight, endHeight, startWidth, endWidth]
CROP_POINTS = {
  "RG": [0, 16, 5, 42],
  "dataExpedicao": [0, 16, 42, 100],
  "nome": [16, 30, 5, 100],
  "filiacao": [30, 47, 5, 100],
  "naturalidade": [47, 59, 5, 50],
  "dataNasc": [47, 59, 50, 100],
  "CPF": [76, 92, 5, 34]
}

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
# Utilizado como base o artigo: http://people.scs.carleton.ca/~roth/iit-publications-iti/docs/gerh-50002.pdf
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
# Utilizado como base o artigo: http://people.scs.carleton.ca/~roth/iit-publications-iti/docs/gerh-50002.pdf
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

          # Checa a borda
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

# Recebe a imagem em array e os 4 pontos em porcentagem do retângulo a ser recortado
# Encontra os pixels relativos a porcentagem enviada
# Gera num novo array com o recorte desejado
def cropImageProportionally(image, startHeight, endHeight, startWidth, endWidth):
  pixelStartHeight = math.floor(imageHeight * (startHeight/100))
  pixelEndHeight = math.floor(imageHeight * (endHeight/100))

  pixelStartWidth = math.floor(imageWidth * (startWidth/100))
  pixelEndWidth = math.floor(imageWidth * (endWidth/100))

  croppedImage = []

  for i in range(pixelStartHeight, pixelEndHeight):
    row = []
    for j in range(pixelStartWidth, pixelEndWidth):
      row.append(image[i][j])
    croppedImage.append(row)

  return croppedImage

def formatText(text, field = 'RG'):
  regex = ''
  text = re.sub(r'\f', '', text)

  if field == "RG":
    regex = r'\d{1,2}.?\d{3}.?\d{3}-?\d{1}|X|x'
  elif field == "CPF":
    # Remove espaços fora e dentro do texto
    cpf = text.replace(" ", "")
    regex = r'[0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2}|[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-/]?[0-9]{2}'
    matchesArray = re.findall(regex, cpf)

    if len(matchesArray) > 0:
      return matchesArray[0]
    else: 
      return None
  elif field == "dataExpedicao" or field == "dataNasc":
    regex = r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'
  elif field == 'nome':
    regex = r"^.{0,4}\n"

    noNameAtStart = re.sub(regex, "", text, 1)

    regex = r"[^A-Z ]+"

    return re.sub(regex, "", noNameAtStart)
  elif field == "naturalidade" or field == "filiacao":
    return text
  
  matchesArray = re.findall(regex, text)

  if len(matchesArray) > 0:
    return matchesArray[0]
  else: 
    return None
      
def pipeline():
  for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
      imageDirectoryPath = OUTPUT_DIR + '/' + filename[:-4]
      fileExtension = filename[-4:]

      # Cria um diretório para cada foto com o nome da mesma
      if not os.path.exists(imageDirectoryPath):
        os.makedirs(imageDirectoryPath)

      print(filename)
      image = cv2.imread(INPUT_DIR + filename) 

      global imageHeight
      imageHeight = len(image)

      global imageWidth
      imageWidth = len(image[0])

      print("Numero de colunas: "+ str(imageWidth))
      print("Numero de linhas: "+ str(imageHeight))
      
      # Passo 1: Converte para escala de cinza
      grayImage = convertToGrayScale(image)
      cv2.imwrite(imageDirectoryPath + "/1-grayImage" + fileExtension, numpy.array(grayImage))
      print("\n*********************************************************************************")
      print("****************************Imagem Cinza gerada**********************************")
      print("*********************************************************************************\n")
      display(Image(imageDirectoryPath + "/1-grayImage" + fileExtension))
      
      # Passo 2: Geramos uma imagem integral
      integralimage = getIntegralImage(grayImage)
      print("Imagem Integral gerada -- Não será exibida pois só é utilizada para criterios de performance")

      # Passo 3: Aplicamos o Threshold Adaptativo
      adaptiveThresholdImage = applyAdaptiveThresholdTest(grayImage, integralimage)
      cv2.imwrite(imageDirectoryPath + "/2-adaptiveThresholdImage" + fileExtension, numpy.array(adaptiveThresholdImage))
      print("\n*********************************************************************************")
      print("**********************Imagem com o Threshold aplicado gerada*********************")
      print("*********************************************************************************\n")
      display(Image(imageDirectoryPath + "/2-adaptiveThresholdImage" + fileExtension))

      outputJSON = {}

      # Passo 4: Recortar a imagem proporcionalmente usando porcentagem
      # Para cada campo do RG recortamos uma nova imagem com base nos 4 pontos definidos no dicionário CROP_POINTS
      # Para cada recorte nós processamos o OCR e salvamos o texto no campo correspondente no outputJSON
      for key, value in CROP_POINTS.items():
        croppedImagePath = imageDirectoryPath + "/3-" + key  + fileExtension

        croppedImage = cropImageProportionally(adaptiveThresholdImage, value[0], value[1], value[2], value[3])

        cv2.imwrite(croppedImagePath, numpy.array(croppedImage))
        print("\n*********************************************************************************")
        print("***************************Imagem recortada: " + key+ "***************************")
        print("*********************************************************************************\n")
        display(Image(croppedImagePath))

        text = pytesseract.image_to_string(cv2.imread(croppedImagePath))
        formattedText = formatText(text, key)

        if(formattedText != None):
          outputJSON[key] = formattedText
        else:
          outputJSON[key] = text

      # Salvamos um arquivo .json com todos os dados do RG requisitados
      with open(imageDirectoryPath + "/4-" + filename[:-4] + ".json" , 'w') as fp:
        json.dump(outputJSON, fp, indent=4, sort_keys=True)
      
      print("\n*********************************************************************************")
      print("********************************JSON Final Gerado********************************")
      print("*********************************************************************************\n")
      print(json.dumps(outputJSON, indent=4, sort_keys=True))

pipeline()