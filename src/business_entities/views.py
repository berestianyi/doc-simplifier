from typing import List

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property

from banks.forms import BankDetailForm
from contracts.models import Contracts
from documents.models import Documents
from .forms import FOPCreateForm, TOVCreateForm, FOPDetailForm, TOVDetailForm, TOVUpdateForm, \
    FOPUpdateForm
from .models import BusinessEntities, BusinessEntitiesEnum
from vehicles.models import Vehicles


class HtmxTemplateMixin:
    htmx_template_name: str = ''

    def get_template_names(self) -> List[str]:
        if self.request.headers.get("HX-Request") == "true" and self.htmx_template_name:
            return [self.htmx_template_name]
        return [self.template_name]


class SortOrderMixin:
    default_sort_field: str = 'created_at'

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


class SearchFilterMixin:
    """
    Миксин для поиска/фильтрации и сортировки BusinessEntities.
    """
    search_param_name = 'searchBusinessEntity'
    entity_type_param_name = 'selectBusinessEntity'
    sort_order_param_name = 'selectDate'

    def get_search_filters(self, search_query):
        return (
            Q(edrpou__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(director_name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(iban__icontains=search_query)
        )

    def filter_queryset(self, queryset):
        request = self.request
        search_query = request.GET.get(self.search_param_name, '').strip()
        entity_type = request.GET.get(self.entity_type_param_name, '')
        sort_order = request.GET.get(self.sort_order_param_name, 'created_at').strip()

        if search_query:
            queryset = queryset.filter(self.get_search_filters(search_query))
        if entity_type:
            queryset = queryset.filter(business_entity=entity_type)

        return queryset.order_by(sort_order)

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class BusinessEntityMixin:
    @cached_property
    def business_entity(self):
        business_entity_id = self.kwargs.get("business_entity_id")
        return get_object_or_404(BusinessEntities, pk=business_entity_id)


def business_entities_list(request):
    business_entities = BusinessEntities.objects.all()
    business_entities_choices = BusinessEntitiesEnum

    search_query = request.GET.get('searchBusinessEntity', '').strip()
    entity_type = request.GET.get('selectBusinessEntity', '')
    sort_order = request.GET.get('selectDate', 'created_at').strip()
    page_number = request.GET.get('page')

    if search_query:
        business_entities = business_entities.filter(
            Q(edrpou__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(director_name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(iban__icontains=search_query)
        )

    if entity_type:
        business_entities = business_entities.filter(
            business_entity=entity_type
        )

    business_entities = business_entities.order_by(sort_order)
    paginator = Paginator(business_entities, 2)
    page_obj = paginator.get_page(page_number)

    context = {
        'business_entities': page_obj,
        'business_entities_choices': business_entities_choices,
        'current_query': request.GET,
    }

    if request.headers.get("HX-Request") == "true":
        return render(request, 'business_entities/partials/list_fields.html', context)

    return render(request, 'business_entities/list.html', context)


def create_fop_form(request):
    fop_form = FOPCreateForm(request.POST or None)
    if request.method == 'POST':

        if fop_form.is_valid():
            fop = fop_form.save(commit=False)
            fop.business_entity = BusinessEntitiesEnum.FOP
            fop.save()

            response = HttpResponse("")
            redirect_url = reverse("business_entities:business_entity_detail", kwargs={"business_entity_id": fop.id})
            response["HX-Redirect"] = redirect_url
            return response

    context = {
        'business_entity_form': fop_form,
        'action': 'create_fop'
    }

    if request.headers.get("HX-Request") == "true":
        return render(request, 'business_entities/partials/create_form.html', context)

    return render(request, 'business_entities/create.html', context)


def create_tov_form(request):
    tov_form = TOVCreateForm(request.POST or None)

    if request.method == 'POST':
        if tov_form.is_valid():
            tov = tov_form.save(commit=False)
            tov.business_entity = BusinessEntitiesEnum.TOV
            tov.save()

            response = HttpResponse("")
            redirect_url = reverse("business_entities:business_entity_detail", kwargs={"business_entity_id": tov.id})
            response["HX-Redirect"] = redirect_url
            return response

    return render(request, 'business_entities/partials/create_form.html', {
        'business_entity_form': tov_form,
        'action': 'create_tov'
    })


def business_entity_detail(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntitiesEnum.FOP:
        business_entity_form = FOPDetailForm(instance=business_entity)
    else:
        business_entity_form = TOVDetailForm(instance=business_entity)

    bank_form = BankDetailForm(instance=business_entity.bank) if business_entity.bank else None

    vehicles_with_entities = (
        Vehicles.objects
        .filter(vehiclelicences__business_entities=business_entity)
        .distinct()
    )

    documents = Documents.objects.filter(
            contract__business_entities=business_entity
        )

    context = {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
        'vehicles_with_entities': vehicles_with_entities,
        'bank_form': bank_form,
        'documents': documents,
    }
    return render(request, 'business_entities/detail.html', context)


def business_entity_detail_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntitiesEnum.FOP:
        business_entity_form = FOPDetailForm(instance=business_entity)
    else:
        business_entity_form = TOVDetailForm(instance=business_entity)

    return render(request, 'business_entities/partials/update_and_detail_form.html', {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
    })


def business_entity_update_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntitiesEnum.FOP:
        business_entity_form = FOPUpdateForm(request.POST or None, instance=business_entity)
    else:
        business_entity_form = TOVUpdateForm(request.POST or None, instance=business_entity)

    if request.method == 'POST':
        if business_entity_form.is_valid():
            updated_business_entity = business_entity_form.save()
            if business_entity.business_entity == BusinessEntitiesEnum.FOP:
                updated_business_entity_form = FOPDetailForm(instance=updated_business_entity)
            else:
                updated_business_entity_form = TOVDetailForm(instance=updated_business_entity)
            return render(request, 'business_entities/partials/update_and_detail_form.html', {
                'business_entity_form': updated_business_entity_form,
                'business_entity': updated_business_entity,
            })

    return render(request, 'business_entities/partials/update_and_detail_form.html', {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
        'action': 'update_business_entity'
    })


def delete_business_entity(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if request.method == 'POST':
        business_entity.delete()
        response = HttpResponse("")
        redirect_url = reverse("business_entities:business_entities")
        response["HX-Redirect"] = redirect_url
        return response
