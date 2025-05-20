from django.urls import path
from src.contracts import views

app_name = 'contracts'

urlpatterns = [
    path('search-forms/<int:business_entity_id>/', views.ContractTemplatesSearchFormView.as_view(),
         name='search_form'),
    path('search/<int:business_entity_id>/', views.ContractTemplatesSearchView.as_view(), name='search'),
    path('create-detail/<int:business_entity_id>/', views.ContractDocumentDetailListView.as_view(),
         name='detail'),
    path('create/<int:business_entity_id>/<int:template_id>', views.ContractCreateView.as_view(), name='create'),
    path('delete/<int:document_id>/<int:business_entity_id>', views.ContractDocumentDeleteView.as_view(),
         name='delete'),
]
