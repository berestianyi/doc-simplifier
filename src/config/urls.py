from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home_page'),
    path("business-entities/", include("business_entities.urls", namespace='business_entities')),
    path("vehicles/", include("vehicles.urls", namespace='vehicles')),
    path('banks/', include('banks.urls', namespace='banks')),
    path('contracts/', include('contracts.urls.contracts_urls', namespace='contracts')),
    path('templates/', include('contracts.urls.templates_urls', namespace='templates')),
    path('users/', include('users.urls', namespace='users')),
    path('documents/', include('documents.urls', namespace='documents')),
]
