from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, UpdateView, TemplateView

from banks.forms import BankDetailForm
from documents.mixins import DocumentMixin
from vehicles.mixins import VehicleMixin
from .forms import FOPCreateForm, TOVCreateForm, FOPDetailForm, TOVDetailForm, TOVUpdateForm, \
    FOPUpdateForm
from .mixins import HtmxMixin, SortOrderMixin, SearchMixin, BusinessEntityMixin
from .models import BusinessEntities, BusinessEntitiesEnum


class BusinessEntitiesListView(
    HtmxMixin,
    SortOrderMixin,
    SearchMixin,
    ListView
):
    model = BusinessEntities
    template_name = 'business_entities/list.html'
    htmx_template_name = 'business_entities/partials/lists/_fields.html'
    context_object_name = 'business_entities'
    paginate_by = 10
    search_param_name = 'searchBusinessEntity'
    entity_type_param_name = 'selectBusinessEntity'
    search_fields = [
        'edrpou',
        'company_name',
        'director_name',
        'address',
        'email',
        'phone',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entities_choices'] = BusinessEntitiesEnum
        context['current_query'] = self.request.GET
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.search_queryset(queryset)
        queryset = self.sort_queryset(queryset)
        entity_type = self.request.GET.get(self.entity_type_param_name, '')
        if entity_type:
            queryset = queryset.filter(business_entity=entity_type)
        return queryset


class FOPCreateView(HtmxMixin, CreateView):
    model = BusinessEntities
    form_class = FOPCreateForm
    template_name = 'business_entities/create.html'
    htmx_template_name = 'business_entities/partials/forms/_fop_create.html'

    def form_valid(self, form):
        business_entity = form.save(commit=False)
        business_entity.business_entity = BusinessEntitiesEnum.FOP
        business_entity.save()
        response = self.htmx_redirect('business_entities:detail', business_entity_id=business_entity.id)
        return response

    def form_invalid(self, form):
        context = self.get_context_data(business_entity_form=form)
        return render(self.request, self.htmx_template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity_form'] = context.pop('form', None)
        return context


class TOVCreateView(HtmxMixin, CreateView):
    model = BusinessEntities
    form_class = TOVCreateForm
    htmx_template_name = 'business_entities/partials/forms/_tov_create.html'

    def form_valid(self, form):
        business_entity = form.save(commit=False)
        business_entity.business_entity = BusinessEntitiesEnum.TOV
        business_entity.save()
        response = self.htmx_redirect('business_entities:detail', business_entity_id=business_entity.id)
        return response

    def form_invalid(self, form):
        context = self.get_context_data(business_entity_form=form)
        return render(self.request, self.htmx_template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity_form'] = context.pop('form', None)
        return context


class BusinessEntityDetailView(HtmxMixin, VehicleMixin, DocumentMixin, BusinessEntityMixin, TemplateView):
    template_name = 'business_entities/detail.html'
    htmx_template_name = 'business_entities/partials/forms/_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity_form'] = self.get_detail_form_class(self.business_entity)(
            instance=self.business_entity)
        context['business_entity'] = self.business_entity
        context['vehicles_with_entities'] = self.vehicles_with_business_entity(self.business_entity)
        context['bank_form'] = BankDetailForm(instance=self.business_entity.bank) if self.business_entity.bank else None
        context['documents'] = self.business_entities_documents(self.business_entity)

        return context


class BusinessEntityUpdateView(BusinessEntityMixin, HtmxMixin, UpdateView):
    model = BusinessEntities
    template_name = 'business_entities/partials/forms/_update.html'

    def get_object(self, queryset=None):
        return self.business_entity

    def get_form_class(self):
        if self.object.business_entity == BusinessEntitiesEnum.FOP:
            return FOPUpdateForm
        return TOVUpdateForm

    def form_valid(self, form):
        self.object = form.save()
        updated_form = self.get_detail_form_class(self.object)(instance=self.object)
        context = {
            'business_entity_form': updated_form,
            'business_entity': self.object,
        }
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'business_entity_form': form,
            'business_entity': self.object,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_update_form_class(self.object)(instance=self.object)
        context['business_entity_form'] = form
        context['business_entity'] = self.object
        return context


class BusinessEntityDeleteView(BusinessEntityMixin,HtmxMixin, View):

    def post(self, request, *args, **kwargs):
        self.business_entity.delete()
        response = self.htmx_redirect('business_entities:list')
        return response
