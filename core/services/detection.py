
from django.conf import settings
from PIL import Image
from core.models.picture import Picture
import numpy as np
import cv2
import easyocr
import os

class Detection:
    """
    Servicio para la detección y procesamiento de texto en imágenes.

    Métodos estáticos:
    - detection(picture_instance): Analiza la instancia de Picture y devuelve los resultados del análisis.
    - processImg(img): Procesa la imagen dada para detectar texto y dibuja las cajas alrededor del texto detectado.
    """
    
    @staticmethod
    def detection(picture_instance: Picture):
        """
        Analiza la instancia de Picture y devuelve los resultados del análisis.

        :param picture_instance: Instancia del modelo Picture
        :return: Diccionario con los resultados del análisis
        """
        path = picture_instance.picture.path
        try:
            with Image.open(path) as img:
                img = np.array(img)
                print(f"Image read successfully with PIL from: {path}")
        except Exception as e:
            print(f"Failed to read image with PIL from: {path}, error: {e}")
            img = None

        if img is not None:
            extracted_text, img_out_url = Detection.processImg(img)
            picture_instance.pictureOutput = img_out_url
            picture_instance.extractedText = extracted_text
            picture_instance.save()
        
        
        
        
    
    @staticmethod
    def processImg(img):  
        """
        Procesa la imagen dada para detectar texto y dibuja las cajas alrededor del texto detectado.

        :param img: Imagen cargada en memoria como un objeto numpy array.
        :return: Nombre del archivo de la imagen procesada.
        :rtype: str

        La función realiza los siguientes pasos:
        1. Utiliza easyocr para detectar texto en la imagen.
        2. Dibuja las cajas de texto detectado en la imagen si la confianza es mayor que un umbral especificado.
        3. Guarda la imagen procesada en el directorio de medios especificado en las configuraciones de Django.
        4. Devuelve el nombre del archivo de la imagen procesada.
        
        **Ejemplo de uso**:
        
        img = cv2.imread('/path/to/image.jpg')
        output_filename = DetectionService.processImg(img)
        """          
        # Instancia del detector de texto
        reader = easyocr.Reader(['es'], gpu=False)
            
        # Detecta texto en la imagen
        text_ = reader.readtext(img)
        
        threshold = 0.25
        extracted_text = ""

        # Dibuja las cajas de texto y el texto detectado en la imagen
        for t_ in text_:
            bbox, text, score = t_
            if score > threshold:
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
                extracted_text += text + " "
        # Guarda la imagen procesada
        output_filename = 'output.png'
        output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
        cv2.imwrite(output_path, img)
            
        return extracted_text.strip(), output_filename