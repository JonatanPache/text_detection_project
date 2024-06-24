from django.test import TestCase, Client
from django.urls import reverse
from core.models import Picture
from core.forms import UploadForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import re

class UploadFormIntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_upload_form_view_get(self):
        """
        Prueba para asegurarse de que el formulario de carga se renderiza correctamente.
        """
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertIsInstance(response.context['formFile'], UploadForm)

    def test_upload_form_view_post(self):
        """
        Prueba para asegurarse de que el formulario de carga procesa la imagen correctamente.
        """
        # Ruta al archivo de imagen de prueba
        image_path = os.path.join(os.path.dirname(__file__), '../mediafiles/test/case_1.jpg')

        # Leer el archivo de imagen de prueba
        with open(image_path, 'rb') as img:
            image = SimpleUploadedFile("case_1.jpg", img.read(), content_type="image/jpeg")

            # Enviar la imagen a través del formulario
            response = self.client.post(reverse('core:home'), {'picture': image})

            # Comprobar que la redirección ocurrió correctamente
            self.assertEqual(response.status_code, 302)

            # Verificar que la imagen se ha guardado en la base de datos
            self.assertEqual(Picture.objects.count(), 1)

            # Verificar que se creó el modelo Picture y que contiene la imagen
            pmodel = Picture.objects.first()
            stored_file_name = pmodel.picture.name
            print(f"Stored file name: {stored_file_name}")  # Verifica el nombre del archivo guardado
            self.assertIn('case_1', stored_file_name)