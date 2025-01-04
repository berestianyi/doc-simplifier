from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('templates', views.ContractTemplatesListView.as_view(), name='templates'),
]
