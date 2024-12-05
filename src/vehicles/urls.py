from django.urls import path
from .views import (
    VehiclesListView,
    VehicleDetailView,
    CreateVehicleView,
)

urlpatterns = [
    path('vehicles/', VehiclesListView.as_view(), name='vehicles'),
    path('vehicles/create/', CreateVehicleView.as_view(), name='create_vehicle'),
    path('vehicles/<int:vehicle_id>/', VehicleDetailView.as_view(), name='vehicle_detail'),
]
