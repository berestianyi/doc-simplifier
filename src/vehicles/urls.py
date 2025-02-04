from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('list/', views.VehiclesListView.as_view(), name='list'),
    path('create/', views.CreateVehicleView.as_view(), name='create'),
    path('create/<int:business_entity_id>/', views.CreateVehicleView.as_view(), name='create_in_business_entity'),
    path('<int:vehicle_id>/', views.VehicleAndLicenceDetailView.as_view(), name='detail'),
    path('<int:vehicle_id>/update/', views.VehicleAndLicenceUpdateView.as_view(), name='update'),
    path('<int:vehicle_id>/delete/', views.VehicleAndLicenceDeleteView.as_view(), name='delete'),
    path('<int:vehicle_id>/redirect-to-detail/',
         views.VehicleRedirectToDetailView.as_view(),
         name='redirect_to_detail'),
    path(
        'create-search-forms/<int:business_entity_id>/',
        views.CreateSearchVehicleFormView.as_view(),
        name='create_search_form',
    ),
    path(
        'search/<int:business_entity_id>/',
        views.SearchVehiclesWithoutEntitiesListView.as_view(),
        name='search_without_entities'
    ),
    path(
        '<int:vehicle_id>/add-to-business-entity/<int:business_entity_id>/',
        views.AddVehicleToBusinessEntityView.as_view(),
        name='add_to_business_entity'
    ),
    path(
        '<int:vehicle_id>/remove-vehicle-from-business-entity/<int:business_entity_id>',
        views.RemoveVehicleFromBusinessEntityView.as_view(),
        name='remove_from_business_entity'
    ),
    path(
        'in-business-entity/<int:business_entity_id>/',
        views.VehiclesInBusinessEntityListView.as_view(),
        name='list_in_business_entity'
    ),
]
