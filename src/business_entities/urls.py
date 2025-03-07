from django.urls import path

from . import views

app_name = 'business_entities'

urlpatterns = [
    path('', views.BusinessEntitiesListView.as_view(), name='list'),
    path('create-fop/', views.FOPCreateView.as_view(), name='create_fop'),
    path('create-tov/', views.TOVCreateView.as_view(), name='create_tov'),
    path('<int:business_entity_id>/', views.BusinessEntityDetailView.as_view(), name='detail'),
    path('delete/<int:business_entity_id>/', views.BusinessEntityDeleteView.as_view(), name='delete'),
    path(
        'update/<int:business_entity_id>/',
        views.BusinessEntityUpdateView.as_view(),
        name='update'
    ),
    path(
        'update/',
        views.BusinessEntityUpdateView.as_view(),
        name='update_'
    )
]
