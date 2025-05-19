from django.urls import path
from .views import generate_pdf, export_to_excel
from . import views

urlpatterns = [
    path('generate-pdf/<int:contract_id>/', generate_pdf, name='generate_pdf'),
    path('export-excel/', export_to_excel, name='export_excel'),
]