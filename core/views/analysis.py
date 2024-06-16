from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from core.models.picture import Picture
from django.template.loader import render_to_string
from weasyprint import HTML

class AnalysisView(generic.TemplateView):
    template_root = "core/"
    template_name = template_root + "analysis.html"

    def get(self, request, pk):
        picture = get_object_or_404(Picture, pk=pk)
        return render(request, self.template_name, {
            "pmodel": picture,
            "ocr": "Texto extraído"  # Reemplaza esto con el OCR real si está disponible
        })

    def post(self, request, pk):
        action = request.POST.get('action')
        if action == 'download_txt':
            return self.download_txt(request, pk)
        elif action == 'download_pdf':
            return self.download_pdf(request, pk)
        else:
            return HttpResponse(status=400)

    def download_txt(self, request, pk):
        picture = get_object_or_404(Picture, pk=pk)
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="output_{pk}.txt"'
        response.write("Texto extraído")  # Reemplaza esto con el OCR real
        return response

    def download_pdf(self, request, pk):
        picture = get_object_or_404(Picture, pk=pk)
        html_string = render_to_string('core/pdf_template.html', {'pmodel': picture, 'ocr': "Texto extraído"})
        html = HTML(string=html_string)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="output_{pk}.pdf"'
        html.write_pdf(response)
        return response
