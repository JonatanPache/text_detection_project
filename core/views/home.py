from django.views import generic
from core.forms.upload import UploadForm
from core.models.picture import Picture
from core.services.detection import Detection
from django.shortcuts import redirect


class HomeView(generic.TemplateView):
    '''
    TemplateView usado para nuestro home.
    
    **Template:**
    
    **Attributes:**
    - `template_root` (str): Directorio base para las plantillas de esta vista.
    - `template_name` (str): Nombre del archivo de plantilla a usar.
    - `form_class` (UploadForm): Formulario utilizado para cargar archivos.

    **Methods:**
    - `post(self, request)`: Maneja las solicitudes POST para cargar y procesar imágenes.
    '''
    template_root = "core/"
    template_name= template_root + "index.html"
    form_class = UploadForm

    def post(self, request):
        '''
        Maneja las solicitudes POST para cargar y procesar imágenes.

        **Parameters:**
        - `request` (HttpRequest): La solicitud HTTP.

        **Returns:**
        - HttpResponse: Renderiza la plantilla `analysis.html` con el modelo de imagen y el texto extraído.

        **Logic:**
        1. Instancia y valida el formulario con los datos de la solicitud.
        2. Si el formulario es válido:
           - Crea una instancia del modelo `Picture` con la imagen subida.
           - Guarda la instancia del modelo `Picture` en la base de datos.
           - Llama al servicio `Detection` para procesar la imagen.
           - Renderiza y devuelve la plantilla `analysis.html` con la información de la imagen procesada y el texto extraído.
        '''
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            pmodel = Picture()
            pmodel.picture = form.cleaned_data['picture']
            pmodel.save()

            # pasamos el modelo al service detection
            Detection.detection(pmodel)

            return redirect('core:analysis', pk=pmodel.pk)
