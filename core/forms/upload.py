from django import forms
from core.models import Picture

class UploadForm(forms.ModelForm):
    """
    Formulario para subir una imagen.

    Atributos:
    ----------
    picture : FileField
        Campo para seleccionar un archivo de imagen.

    Meta:
    -----
    model : Picture
        Modelo asociado al formulario.
    fields : list
        Lista de campos del modelo que se incluirán en el formulario.
    """

    picture = forms.FileField()
    """
    Campo para seleccionar un archivo de imagen.

    widget : FileInput
        Tipo de widget que se utilizará para representar el campo en el navegador.
    """

    class Meta:
        model = Picture
        """
        Modelo asociado al formulario.

        model : Picture
            Modelo de Django al que está asociado este formulario.
        """
        fields = ['picture']
        """
        Lista de campos del modelo que se incluirán en el formulario.

        fields : list
            Lista de campos del modelo que se mostrarán en el formulario.
        """
