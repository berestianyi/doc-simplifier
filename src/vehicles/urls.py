from django.urls import path
from .views import (
    VehiclesListView,
    CreateVehicleView,
    vehicles_detail,
    delete_vehicle_and_licence,
    submit_vehicle_and_licence_update_form,
    create_vehicle_and_licence_update_form,
)

urlpatterns = [
    path('vehicles/', VehiclesListView.as_view(), name='vehicles'),
    path('vehicles/create/', CreateVehicleView.as_view(), name='create_vehicle'),
    path('vehicles/<int:vehicle_id>/', vehicles_detail, name='vehicle_detail'),
    path('vehicles/delete/<int:vehicle_id>/', delete_vehicle_and_licence, name='delete_vehicle_and_licence'),
    path(
        'vehicles/htmx/create-vehicle-and-licence-update-form/<int:vehicle_id>/',
        create_vehicle_and_licence_update_form,
        name='create_vehicle_and_licence_update_form'
    ),
    path(
        'vehicles/htmx/submit-vehicle-and-licence-update-form/<int:vehicle_id>/',
        submit_vehicle_and_licence_update_form,
        name='submit_vehicle_and_licence_update_form'
    ),
]
