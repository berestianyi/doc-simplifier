from django.urls import path
from . import views

app_name = 'banks'

urlpatterns = [
    path('search-form/<int:business_entity_id>/', views.create_bank_search_form, name='create_bank_search_form'),
    path('search/<int:business_entity_id>/', views.search_banks, name='search_banks'),
    path('add/<int:business_entity_id>/<int:bank_id>/', views.add_bank_to_business_entity,
         name='add_bank_to_business_entity'),
    path('detail-form/<int:business_entity_id>/', views.create_bank_detail_form, name='create_bank_detail_form'),
    path('create-form/<int:business_entity_id>/', views.create_bank_form, name='create_bank_form'),
    path('submit-form/<int:business_entity_id>/', views.create_bank_form, name='submit_bank_form'),
    path('update-form/<int:business_entity_id>/', views.update_bank_form, name='update_bank_form'),
    path('delete/<int:business_entity_id>/', views.delete_bank, name='delete_bank'),
]
