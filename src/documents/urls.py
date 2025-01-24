from django.urls import path

from documents import views

app_name = 'documents'


urlpatterns = [
    path('pdf-extract', views.PDFUploadView.as_view(), name='pdf-extract'),
    path('documents/download/<int:pk>/', views.DocumentsDownloadView.as_view(), name='documents_download'),
]