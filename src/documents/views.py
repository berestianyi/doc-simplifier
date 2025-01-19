from django.shortcuts import render
from django.views.generic import ListView

from business_entities.views import BusinessEntityMixin
from .models import Documents


class DocumentsDetailListView(BusinessEntityMixin, ListView):
    model = Documents
    template_name = 'documents/detail_list.html'
    context_object_name = 'documents'
    paginate_by = 5

    def get_queryset(self):
        return Documents.objects.filter(
            contract__business_entities=self.business_entity
        )
