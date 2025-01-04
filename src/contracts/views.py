from django.shortcuts import render
from django.views.generic import ListView

from .models import Templates


class ContractTemplatesListView(ListView):
    model = Templates
    template_name = 'contract_templates/list.html'
    context_object_name = 'templates'
    paginate_by = 10

