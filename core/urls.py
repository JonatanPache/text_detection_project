from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('analysis/<uuid:pk>/', views.AnalysisView.as_view(), name='analysis'),
    # path('download/txt/<int:pk>/', download_txt, name='download_txt'),
    # path('download/pdf/<int:pk>/', download_pdf, name='download_pdf'),
]
