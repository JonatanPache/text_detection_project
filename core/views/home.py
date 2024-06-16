from django.views import generic
from core.forms.upload import UploadForm
from core.models.picture import Picture
from core.services.detection import Detection
from django.shortcuts import render


class HomeView(generic.TemplateView):
    '''
    TemplateView usado para nuestro home.
    
    **Template:**
    
    :template:`core`
    '''
    template_root = "core/"
    template_name= template_root + "index.html"
    form_class = UploadForm

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            pmodel = Picture()
            pmodel.picture = form.cleaned_data['picture']
            pmodel.save()

            # pasamos el modelo al service detection
            #Detection.detection(pmodel)

            return render(request, self.template_root+'analysis.html', {
                "pmodel": pmodel,
                "ocr": "Texto extraído"
            })
