from django.urls import path
from . import views

app_name = 'banks'

urlpatterns = [
    path('search-form/<int:business_entity_id>/', views.BankSearchCreateFormView.as_view(), name='create_bank_search_form'),
    path('search/<int:business_entity_id>/', views.BankSearchListView.as_view(), name='search_banks'),
    path('add/<int:business_entity_id>/<int:bank_id>/', views.AddBankToBusinessEntityView.as_view(),
         name='add_bank_to_business_entity'),
    path('detail-form/<int:business_entity_id>/', views.BankDetailView.as_view(), name='create_bank_detail_form'),
    path('create-form/<int:business_entity_id>/', views.BankCreateView.as_view(), name='create_bank_form'),
    path('submit-form/<int:business_entity_id>/', views.BankCreateView.as_view(), name='submit_bank_form'),
    path('update-form/<int:business_entity_id>/', views.BankUpdateView.as_view(), name='update_bank_form'),
    path('delete/<int:business_entity_id>/', views.BankDeleteView.as_view(), name='delete_bank'),
]
