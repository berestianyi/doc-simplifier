from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('templates', views.ContractTemplatesListView.as_view(), name='templates'),
    path('search-form/<int:business_entity_id>/', views.create_contract_templates_search_form,
         name='create_contract_templates_search_form'),
    path('search/<int:business_entity_id>/', views.search_contract_templates, name='search_contract_templates'),
    path('create-detail/<int:business_entity_id>/', views.create_document_detail_list,
         name='create_document_detail_list'),
    path('create/<int:business_entity_id>/<int:template_id>', views.create_contract, name='create_contract'),
    path('templates/create/', views.create_template, name='create_template'),
    path('templates/update/<int:template_id>/', views.update_template, name='update_template'),
    path('templates/download/<int:pk>/', views.TemplatesDownloadView.as_view(), name='templates_download'),
    path('redirect-to-templates/', views.redirect_to_templates_list, name='redirect_to_templates_list'),
]
