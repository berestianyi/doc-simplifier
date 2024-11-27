from django.urls import path

from business_entities import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('business-entities', views.business_entities, name='business_entities'),
]
