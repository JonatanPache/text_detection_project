"""
Este módulo contiene pruebas unitarias para la clase Detection y sus métodos relacionados.

Las pruebas cubren la detección de texto en imágenes, el procesamiento de imágenes,
y el manejo de casos especiales como imágenes inválidas o sin texto.
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models.picture import Picture
from core.services.detection import Detection
import os
import numpy as np
from PIL import Image
from django.conf import settings


class DetectionTestCase(TestCase):
    """
    Clase de prueba para la funcionalidad de detección de texto en imágenes.

    Esta clase prueba varios aspectos de la detección de texto, incluyendo
    el procesamiento de imágenes válidas, el manejo de imágenes inválidas,
    y el comportamiento con imágenes sin texto.
    """
    def setUp(self):
        """Configura el entorno de prueba antes de cada test."""
        self.test_dir = os.path.dirname(__file__)
        self.test_image_path = os.path.join(
            self.test_dir, "../../mediafiles/test/test1.jpg"
        )
        self.output_dir = os.path.join(self.test_dir, "../../mediafiles/test/output")

        # Crear el directorio de salida si no existe
        os.makedirs(self.output_dir, exist_ok=True)

        # Crear una instancia de Picture con la imagen de prueba
        with open(self.test_image_path, "rb") as img_file:
            self.picture = Picture.objects.create(
                picture=SimpleUploadedFile(
                    name="test1.jpg", content=img_file.read(), content_type="image/jpeg"
                )
            )

    def test_detection_method(self):
        """Prueba el método de detección principal."""
        Detection.detection(self.picture)

        self.assertIsNotNone(self.picture.extractedText)
        self.assertIn("2534RIS", self.picture.extractedText)
        self.assertIsNotNone(self.picture.pictureOutput)
        self.assertTrue(os.path.exists(self.picture.pictureOutput.path))

    def test_processImg_method(self):
        """Prueba el método de procesamiento de imagen."""
        img = np.array(Image.open(self.picture.picture.path))

        extracted_text, output_filename = Detection.processImg(img)

        # Verificar que se haya extraído texto
        self.assertIsInstance(extracted_text, str)
        
        # Verificar que el texto extraído contiene el número de placa esperado
        self.assertIn("2534RIS", extracted_text)
        
        # Verificar que se haya generado un nombre de archivo de salida
        self.assertEqual(output_filename, 'output.png')

        # Verificar que el archivo de salida exista en la ubicación correcta
        expected_output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
        
        print(f"Expected output path: {expected_output_path}")
        print(f"File exists: {os.path.exists(expected_output_path)}")

        self.assertTrue(os.path.exists(expected_output_path), 
                        f"Output file not found at {expected_output_path}")

        # Verificar que la imagen de salida es válida
        try:
            output_img = Image.open(expected_output_path)
            self.assertIsNotNone(output_img)
        except Exception as e:
            self.fail(f"Failed to open output image: {str(e)}")

        self.assertEqual(output_img.size, Image.open(self.picture.picture.path).size)


    def test_detection_with_invalid_image(self):
        """Prueba la detección con una imagen inválida."""
        invalid_picture = Picture.objects.create(
            picture=SimpleUploadedFile(
                name="invalid.txt",
                content=b"invalid content",
                content_type="text/plain",
            )
        )

        try:
            Detection.detection(invalid_picture)
        except Exception as e:
            self.fail(f"Detection.detection() raised {type(e).__name__} unexpectedly!")
        self.assertIsNone(invalid_picture.extractedText)


    def test_detection_with_no_text(self):
        """Prueba la detección en una imagen sin texto."""
        img = Image.new("RGB", (100, 100), color="blue")
        img_path = os.path.join(self.test_dir, "no_text.png")
        img.save(img_path)

        with open(img_path, "rb") as img_file:
            no_text_picture = Picture.objects.create(
                picture=SimpleUploadedFile(
                    name="no_text.png",
                    content=img_file.read(),
                    content_type="image/png",
                )
            )

        Detection.detection(no_text_picture)
        self.assertEqual(no_text_picture.extractedText, "")


    def tearDown(self):
        """Limpia el entorno después de cada prueba."""
        no_text_path = os.path.join(self.test_dir, "no_text.png")
        if os.path.exists(no_text_path):
            os.remove(no_text_path)

        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
