from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from utils.model import Model

class Picture(ActivatorModel, TimeStampedModel, Model):

    class Meta:
        verbose_name_plural = "pictures"

    picture = models.FileField(upload_to='pictures', blank=True)

    pictureOutput = models.FileField(upload_to='pictureSalida', blank=True)

    extractedText = models.TextField(blank=True, null=True)