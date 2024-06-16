# ocr_app/views.py

import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import UploadImageForm
import cv2
import easyocr

def index(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(file_path)
            
            # Ruta completa de la imagen
            image_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Lee la imagen
            img = cv2.imread(image_path)
            if img is None:
                return render(request, 'ocr_app/index.html', {'form': form, 'error': 'No se pudo leer la imagen.'})
            
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
            output_path = os.path.join(settings.MEDIA_ROOT, 'output.png')
            cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            return render(request, 'ocr_app/index.html', {
                'form': form, 
                'file_url': file_url, 
                'output_url': fs.url('output.png')
            })
    else:
        form = UploadImageForm()
    return render(request, 'ocr_app/index.html', {'form': form})
