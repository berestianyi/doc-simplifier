from django.urls import path
from . import views

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

]
