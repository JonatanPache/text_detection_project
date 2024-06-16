# --------------------------
#   python imports
# --------------------------
import uuid


# --------------------------
#   django imports
# --------------------------
from django.db import models
from django.utils.translation import gettext_lazy as _


class Model(models.Model):
    '''
    Usamos para cada entidad
    '''
    id=models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4
        )
    
    class Meta:
        abstract=True