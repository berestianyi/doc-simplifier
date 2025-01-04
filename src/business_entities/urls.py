from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home_page'),
    path('business-entities/', views.BusinessEntitiesListView.as_view(), name='business_entities'),
    path('business-entity/create/', views.create_business_entity, name='create_business_entity'),
    path('business-entity/create-fop-form/', views.create_fop_form, name='create_fop_form'),
    path('business-entity/create-tov-form/', views.create_tov_form, name='create_tov_form'),
    path('business-entity/submit-fop-form/', views.submit_fop_form, name='submit_fop_form'),
    path('business-entity/submit-tov-form/', views.submit_tov_form, name='submit_tov_form'),
    path('business-entity/<int:business_entity_id>/', views.business_entity_detail, name='business_entity_detail'),
    path('business-entity/delete/<int:business_entity_id>/', views.delete_business_entity, name='delete_business_entity'),
    path(
        'business-entity/create-update-form/<int:business_entity_id>/',
        views.create_business_entity_update_form,
        name='create_business_entity_update_form'
    ),
    path(
        'business-entity/create-detail-form/<int:business_entity_id>/',
        views.create_business_entity_detail_form,
        name='create_business_entity_detail_form'
    ),
    path(
        'business-entity/submit-update-form/<int:business_entity_id>/',
        views.submit_business_entity_update_form,
        name='submit_business_entity_update_form'),
    path(
        'business-entity/create_search_vehicle_form/<int:business_entity_id>/',
        views.create_search_vehicle_form,
        name='create_search_vehicle_form',
    ),
    path(
        'business-entity/search_vehicles/<int:business_entity_id>/',
        views.search_vehicles_without_entities,
        name='search_vehicles_without_entities'
    ),
    path(
        'business-entity/<int:business_entity_id>/add-vehicle/<int:vehicle_id>/',
        views.add_vehicle_to_business_entity,
        name='add_vehicle_to_business_entity'
    ),
    path(
        'business-entity/<int:business_entity_id>/remove-vehicle/<int:vehicle_id>/',
        views.remove_vehicle_from_business_entity,
        name='remove_vehicle_from_business_entity'
    ),
    path(
        'business-entity/<int:business_entity_id>/vehicles/',
        views.vehicles_in_business_entity,
        name='vehicles_in_business_entity'
    ),
]
