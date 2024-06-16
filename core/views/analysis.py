from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from core.models.picture import Picture
from django.template.loader import render_to_string
from weasyprint import HTML

class AnalysisView(generic.TemplateView):
    """
    View para manejar el análisis y descarga de resultados para una instancia de Picture.

    Métodos:
    --------
    get(self, request, pk):
        Maneja las solicitudes GET para mostrar la página de análisis.

    post(self, request, pk):
        Maneja las solicitudes POST para descargar archivos (PDF o TXT).

    download_txt(self, request, pk):
        Genera y devuelve un archivo de texto para descargar.

    download_pdf(self, request, pk):
        Genera y devuelve un archivo PDF para descargar.
    """

    template_root = "core/"
    template_name = template_root + "analysis.html"

    def get(self, request, pk):
        """
        Maneja las solicitudes GET para mostrar la página de análisis.

        Parámetros:
        -----------
        request : HttpRequest
            Objeto HttpRequest que representa la solicitud HTTP.

        pk : int
            Clave primaria de la instancia de Picture a analizar.

        Retorna:
        --------
        HttpResponse
            Respuesta HTTP que renderiza la plantilla de análisis con los datos de la instancia de Picture y OCR.

        Lanza:
        ------
        Http404
            Si no se encuentra la instancia de Picture con la clave primaria dada.
        """
        picture = get_object_or_404(Picture, pk=pk)
        return render(request, self.template_name, {
            "pmodel": picture,
            "ocr": "Texto extraído"  # Reemplaza esto con el OCR real si está disponible
        })

    def post(self, request, pk):
        """
        Maneja las solicitudes POST para descargar archivos (PDF o TXT).

        Parámetros:
        -----------
        request : HttpRequest
            Objeto HttpRequest que representa la solicitud HTTP.

        pk : int
            Clave primaria de la instancia de Picture a analizar.

        Retorna:
        --------
        HttpResponse
            Respuesta HTTP que devuelve un archivo PDF o TXT para descargar.

        Lanza:
        ------
        HttpResponseBadRequest
            Si la acción solicitada en el formulario POST no es válida.
        """
        action = request.POST.get('action')
        if action == 'download_txt':
            return self.download_txt(request, pk)
        elif action == 'download_pdf':
            return self.download_pdf(request, pk)
        else:
            return HttpResponse(status=400)

    def download_txt(self, request, pk):
        """
        Genera y devuelve un archivo de texto para descargar.

        Parámetros:
        -----------
        request : HttpRequest
            Objeto HttpRequest que representa la solicitud HTTP.

        pk : int
            Clave primaria de la instancia de Picture a analizar.

        Retorna:
        --------
        HttpResponse
            Respuesta HTTP que devuelve un archivo de texto para descargar.

        Lanza:
        ------
        Http404
            Si no se encuentra la instancia de Picture con la clave primaria dada.
        """
        picture = get_object_or_404(Picture, pk=pk)
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="output_{pk}.txt"'
        response.write("Texto extraído")  # Reemplaza esto con el OCR real
        return response

    def download_pdf(self, request, pk):
        """
        Genera y devuelve un archivo PDF para descargar.

        Parámetros:
        -----------
        request : HttpRequest
            Objeto HttpRequest que representa la solicitud HTTP.

        pk : int
            Clave primaria de la instancia de Picture a analizar.

        Retorna:
        --------
        HttpResponse
            Respuesta HTTP que devuelve un archivo PDF para descargar.

        Lanza:
        ------
        Http404
            Si no se encuentra la instancia de Picture con la clave primaria dada.
        """
        picture = get_object_or_404(Picture, pk=pk)
        html_string = render_to_string('core/pdf_template.html', {'pmodel': picture, 'ocr': "Texto extraído"})
        html = HTML(string=html_string)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="output_{pk}.pdf"'
        html.write_pdf(response)
        return response
