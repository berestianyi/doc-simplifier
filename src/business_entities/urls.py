from django.urls import path

from . import views

app_name = 'business_entities'

urlpatterns = [
    path('', views.business_entities_list, name='business_entities'),
    path('create-fop-form/', views.create_fop_form, name='create_fop_form'),
    path('create-tov-form/', views.create_tov_form, name='create_tov_form'),
    path('<int:business_entity_id>/', views.business_entity_detail, name='business_entity_detail'),
    path('delete/<int:business_entity_id>/', views.delete_business_entity, name='delete_business_entity'),
    path(
        'update-form/<int:business_entity_id>/',
        views.business_entity_update_form,
        name='business_entity_update_form'
    ),
    path(
        'detail-form/<int:business_entity_id>/',
        views.business_entity_detail_form,
        name='business_entity_detail_form'
    ),
]
