from django.urls import path, include

urlpatterns = [
    path("", include("business_entities.urls")),
    path("", include("vehicles.urls")),
    path('banks/', include('banks.urls', namespace='banks')),
    path('contracts/', include('contracts.urls', namespace='contracts')),
]
