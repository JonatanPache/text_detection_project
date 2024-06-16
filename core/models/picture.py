from django.db import models
from utils.model import Model
from django_extensions.db.models import ActivatorModel, TimeStampedModel

class Picture(ActivatorModel, TimeStampedModel, Model):
    class Meta:
        verbose_name_plural="pictures"
    
    picture = models.FileField(upload_to='pictures', blank=True)
    pictureOutput = models.FileField(upload_to='pictureSalida',blank=True)