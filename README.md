Objetivo
Desenvolver uma API que por meio de uma chamada POST
    - Receber a imagem do RG
    - Faça algumas melhorias na imagem
    - Enviar para uma API de OCR para extrair as informações 
    - Retornar um JSON com todas as infos do RG


Etapas para a melhoria da imagem
    - Converter para escala de cinza
    - Aplicar binarização
    - Indentificar bordas do RG
    - Cortar a imagem em subseções


{
    "RG": "55.555.555-00",
    "dataExpedicao": "11/11/2011",
    "nome": "Alexandre",
    "filiacao": "Alcebiades Brian\n Stenifer Johanneson",
    "naturalidade": "S.Paulo - SP",
    "dataNasc": "11/11/1990",
    "docOrigem": "Barueri SP ...",
    "CPF": "294948348/37"
}