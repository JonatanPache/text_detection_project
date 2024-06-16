from django import forms

from core.models import Picture

class UploadForm(forms.ModelForm):
    picture = forms.FileField()
    class Meta:
        model = Picture
        fields = ['picture']
    

    '''
    class Meta:
        model = Picture
        fields = ('picture')'''