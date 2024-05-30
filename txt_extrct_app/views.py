'''
----------- views.py ------------

Autor: Yonatan Condori Pacheco
Fecha: 29-05-2024

Descripcion: Todos los metodos que utiliza home.html
'''

# Importacion de paquetes defult
import base64
from django.contrib import messages
from django.shortcuts import render
from PIL import Image

# Paquetes para el analisis
import numpy as np
import pytesseract  

# En caso de windows, primero instalar desde - https://github.com/UB-Mannheim/tesseract/wiki y luego
# descomentar la siguinete linea, y comentar la linea de para linux
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
# )

# solo para linux, hace referencia al ejecutable 
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


'''
homepage()
params: request // solo POST

Analiza la imagen seleccionado para devolver en formato texto.

0. Si el request no es POST, entonces solo renderiza home.html

1. Si no ha seleccionado ninguna imagen devolver un error message, y renderizamos

2. Caso contrario, procede al analisis de la imagen
    2.1. Actualiza el lenguaje seleccionado em lang
    2.2. Almacena la imagen en un array en la variable img
    2.3. Utilizamos la funcion image_to_string de pytesseract, con los parametros correspondientes para
    obtener el texto y asignarlo a la variable text.
    2.4.renderizamos a home.html devolviendo los datos obtenidos de la imagen
'''
def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "Imagen no seleccionado"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "home.html", {"ocr": text, "image": image_base64})

    return render(request, "home.html")
