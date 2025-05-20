from django.urls import path
from src.contracts import views

app_name = 'templates'

urlpatterns = [
    path('', views.ContractTemplatesListView.as_view(), name='list'),
    path('create/', views.TemplateCreateView.as_view(), name='create'),
    path('update/<int:template_id>/', views.TemplateUpdateView.as_view(), name='update'),
    path('download/<int:template_id>/', views.TemplatesDownloadView.as_view(), name='download'),
]
