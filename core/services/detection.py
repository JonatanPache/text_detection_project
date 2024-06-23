
from django.conf import settings

from core.models.picture import Picture

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
    def detection(picture_instance):
        """
        Analiza la instancia de Picture y devuelve los resultados del análisis.

        :param picture_instance: Instancia del modelo Picture
        :return: Diccionario con los resultados del análisis
        """
        img = cv2.imread(picture_instance.picture.path)
        img_out_url =  Detection.processImg(img)
        picture_instance.pictureOutput = img_out_url
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
        reader = easyocr.Reader(['en'], gpu=False)
            
        # Detecta texto en la imagen
        text_ = reader.readtext(img)
        
        threshold = 0.25
            
        # Dibuja las cajas de texto y el texto detectado en la imagen
        for t_ in text_:
            bbox, text, score = t_
            if score > threshold:
                cv2.rectangle(img, tuple(bbox[0]), tuple(bbox[2]), (0, 255, 0), 2)
                cv2.putText(img, text, tuple(bbox[0]), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
            
        # Guarda la imagen procesada
        output_filename = 'output.png'
        output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
        cv2.imwrite(output_path, img)
            
        return output_filename