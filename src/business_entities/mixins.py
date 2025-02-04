from typing import List

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property

from .forms import FOPCreateForm, TOVCreateForm, FOPUpdateForm, TOVUpdateForm, FOPDetailForm, TOVDetailForm
from .models import BusinessEntities, BusinessEntitiesEnum


class BusinessEntityMixin:
    @cached_property
    def business_entity(self):
        business_entity_id = self.kwargs.get("business_entity_id")
        if business_entity_id is None:
            return None
        return get_object_or_404(BusinessEntities, pk=business_entity_id)

    @staticmethod
    def get_create_form_class(business_entity):
        if business_entity.business_entity == BusinessEntitiesEnum.FOP:
            return FOPCreateForm
        return TOVCreateForm

    @staticmethod
    def get_update_form_class(business_entity):
        if business_entity.business_entity == BusinessEntitiesEnum.FOP:
            return FOPUpdateForm
        return TOVUpdateForm

    @staticmethod
    def get_detail_form_class(business_entity):
        if business_entity.business_entity == BusinessEntitiesEnum.FOP:
            return FOPDetailForm
        return TOVDetailForm


class HtmxMixin:
    htmx_template_name: str = ''

    def get_template_names(self) -> List[str]:
        if self.request.headers.get("HX-Request") == "true" and self.htmx_template_name:
            return [self.htmx_template_name]
        return [self.template_name]

    @staticmethod
    def htmx_redirect(to: str, **kwargs) -> HttpResponse:
        response = HttpResponse(status=204)
        redirect_url = reverse(to, kwargs=kwargs)
        response["HX-Redirect"] = redirect_url
        return response


class SortOrderMixin:
    default_sort_field: str = '-created_at'

    def get_sort_field(self) -> str:
        return self.request.GET.get('selectDate', self.default_sort_field).strip()

    def sort_queryset(self, queryset):
        sort_field = self.get_sort_field()
        return queryset.order_by(sort_field)


class SearchMixin:
    search_param_name: str = ''
    search_fields: List[str] = []

    def get_search_query(self) -> str:
        return self.request.GET.get(self.search_param_name, '').strip()

    def build_search_filters(self, search_query: str) -> Q:
        q_object = Q()
        for field_name in self.search_fields:
            q_object |= Q(**{f"{field_name}__icontains": search_query})
        return q_object

    def search_queryset(self, queryset):
        search_query = self.get_search_query()
        if search_query:
            filters = self.build_search_filters(search_query)
            queryset = queryset.filter(filters)
        return queryset
