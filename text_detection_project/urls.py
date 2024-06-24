# text_detection_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import sys

urlpatterns = [
    path("", include('core.urls')),
    path('admin/', admin.site.urls),
    # path("__debug__/", include('debug_toolbar.urls')),
    # path('', include('ocr_app.urls')), #no working
] 

if settings.PRODUCTION:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG and 'test' not in sys.argv:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns