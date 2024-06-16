from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from utils.model import Model

class Picture(ActivatorModel, TimeStampedModel, Model):
    """
    Modelo para almacenar información relacionada con las imágenes y sus salidas.

    Atributos:
    ----------
    picture : FileField
        Campo para almacenar la imagen original.

    pictureOutput : FileField
        Campo para almacenar la imagen procesada o de salida.
    """

    class Meta:
        verbose_name_plural = "pictures"
        """
        Opciones meta del modelo:
        
        verbose_name_plural : str
            Nombre en plural amigable para humanos del modelo en el administrador de Django.
        """

    picture = models.FileField(upload_to='pictures', blank=True)
    """
    Campo para almacenar la imagen original.

    upload_to : str
        Directorio relativo donde se almacenarán las imágenes.
    blank : bool
        Indica si el campo puede estar en blanco en los formularios (True) o no (False).
    """

    pictureOutput = models.FileField(upload_to='pictureSalida', blank=True)
    """
    Campo para almacenar la imagen procesada o de salida.

    upload_to : str
        Directorio relativo donde se almacenarán las imágenes de salida.
    blank : bool
        Indica si el campo puede estar en blanco en los formularios (True) o no (False).
    """
