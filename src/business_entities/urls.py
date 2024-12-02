from django.urls import path

from business_entities import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('business-entities', views.business_entities, name='business_entities'),
    path('business-entity', views.business_entity, name='business_entity'),
    path('create-business-entity', views.create_business_entity, name='create_business_entity'),
]
