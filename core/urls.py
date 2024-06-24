from django.urls import path
from . import views

app_name = 'core'
"""
Nombre de la aplicación: 'core'

app_name : str
    Nombre asignado a la aplicación para evitar conflictos de nombres de URL entre diferentes aplicaciones.
"""

urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),

    path('analysis/<uuid:pk>/', views.AnalysisView.as_view(), name='analysis'),

]
