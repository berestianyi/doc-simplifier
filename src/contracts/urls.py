from django.urls import path
from . import views
from documents.views import DocumentsDownloadView

app_name = 'contracts'

urlpatterns = [
    path('templates', views.ContractTemplatesListView.as_view(), name='templates'),
    path('search-form/<int:business_entity_id>/', views.ContractTemplatesSearchFormView.as_view(),
         name='create_contract_templates_search_form'),
    path('search/<int:business_entity_id>/', views.ContractTemplatesSearchView.as_view(), name='search_contract_templates'),
    path('create-detail/<int:business_entity_id>/', views.ContractDocumentDetailListView.as_view(),
         name='create_document_detail_list'),
    path('create/<int:business_entity_id>/<int:template_id>', views.ContractCreateView.as_view(), name='create_contract'),
    path('templates/create/', views.TemplateCreateView.as_view(), name='create_template'),
    path('templates/update/<int:template_id>/', views.TemplateUpdateView.as_view(), name='update_template'),
    path('templates/download/<int:pk>/', views.TemplatesDownloadView.as_view(), name='templates_download'),
    path('documents/download/<int:pk>/', DocumentsDownloadView.as_view(), name='documents_download'),
    path('redirect-to-templates/', views.TemplatesListRedirectView.as_view(), name='redirect_to_templates_list'),
]
