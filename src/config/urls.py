from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home_page'),
    path('error/', TemplateView.as_view(template_name="error.html"), name='error_page'),
    path("business-entities/", include("src.business_entities.urls", namespace='business_entities')),
    path("vehicles/", include("src.vehicles.urls", namespace='vehicles')),
    path('banks/', include('src.banks.urls', namespace='banks')),
    path('contracts/', include('src.contracts.urls.contracts_urls', namespace='contracts')),
    path('templates/', include('src.contracts.urls.templates_urls', namespace='templates')),
    path('users/', include('src.users.urls', namespace='users')),
    path('documents/', include('src.documents.urls', namespace='documents')),
]
