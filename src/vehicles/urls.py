from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('vehicles/', views.VehiclesListView.as_view(), name='vehicles'),
    path('vehicles/create/', views.CreateVehicleView.as_view(), name='create_vehicle'),
    path('vehicles/<int:vehicle_id>/', views.vehicles_detail, name='vehicle_detail'),
    path('vehicles/delete/<int:vehicle_id>/', views.delete_vehicle_and_licence, name='delete_vehicle_and_licence'),
    path(
        'vehicles/create-vehicle-and-licence-update-form/<int:vehicle_id>/',
        views.create_vehicle_and_licence_update_form,
        name='create_vehicle_and_licence_update_form'
    ),
    path(
        'vehicles/submit-vehicle-and-licence-update-form/<int:vehicle_id>/',
        views.submit_vehicle_and_licence_update_form,
        name='submit_vehicle_and_licence_update_form'
    ),
    path('vehicle/<int:vehicle_id>/redirect-to-detail/',
         views.redirect_to_vehicle_detail,
         name='redirect_to_vehicle_detail'),

    path(
        'vehicle/redirect-to-create/',
        views.redirect_to_vehicle_create_form,
        name='redirect_to_vehicle_create_form'
    ),
path(
        'create_search_vehicle_form/<int:business_entity_id>/',
        views.create_search_vehicle_form,
        name='create_search_vehicle_form',
    ),
    path(
        'search_vehicles/<int:business_entity_id>/',
        views.search_vehicles_without_entities,
        name='search_vehicles_without_entities'
    ),
    path(
        '<int:business_entity_id>/add-vehicle/<int:vehicle_id>/',
        views.add_vehicle_to_business_entity,
        name='add_vehicle_to_business_entity'
    ),
    path(
        '<int:business_entity_id>/remove-vehicle/<int:vehicle_id>/',
        views.remove_vehicle_from_business_entity,
        name='remove_vehicle_from_business_entity'
    ),
    path(
        '<int:business_entity_id>/vehicles/',
        views.vehicles_in_business_entity,
        name='vehicles_in_business_entity'
    ),
]
