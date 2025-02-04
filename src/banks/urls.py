from django.urls import path
from . import views

app_name = 'banks'

urlpatterns = [
    path('search-forms/<int:business_entity_id>/', views.BankSearchCreateFormView.as_view(), name='search_form'),
    path('search/<int:business_entity_id>/', views.BankSearchListView.as_view(), name='search'),
    path('add/<int:business_entity_id>/<int:bank_id>/', views.AddBankToBusinessEntityView.as_view(),
         name='add_to_business_entity'),
    path('detail-forms/<int:business_entity_id>/', views.BankDetailView.as_view(), name='detail'),
    path('create-forms/<int:business_entity_id>/', views.BankCreateView.as_view(), name='create'),
    path('update-forms/<int:business_entity_id>/', views.BankUpdateView.as_view(), name='update'),
    path('delete/<int:business_entity_id>/', views.BankDeleteView.as_view(), name='delete'),
]
