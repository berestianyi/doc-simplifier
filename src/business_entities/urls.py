from django.urls import path
from .views import (
    HomePageView,
    BusinessEntitiesListView,
    BusinessEntityDetailView,
    CreateBusinessEntityView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('business-entities/', BusinessEntitiesListView.as_view(), name='business_entities'),
    path('business-entity/<int:entity_id>/', BusinessEntityDetailView.as_view(), name='business_entity_detail'),
    path('business-entity/create/', CreateBusinessEntityView.as_view(), name='create_business_entity'),
]