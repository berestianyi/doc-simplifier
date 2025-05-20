from django.urls import path

from . import views

app_name = 'documents'


urlpatterns = [
    path('pdf-extract', views.PDFUploadView.as_view(), name='pdf-extract'),
    path('documents/download/<int:document_id>/', views.DocumentsDownloadView.as_view(), name='download'),
]
