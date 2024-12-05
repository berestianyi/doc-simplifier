from django.urls import path, include

urlpatterns = [
    path("", include("business_entities.urls")),
    path("", include("vehicles.urls")),
]
