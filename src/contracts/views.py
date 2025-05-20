from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, UpdateView

from src.business_entities.mixins import SearchMixin
from src.business_entities.views import BusinessEntityMixin
from src.documents.mixins import DocumentMixin
from src.documents.models import Documents
from src.vehicles.mixins import VehicleMixin
from .forms import TemplatesForm, RoyalForm, RolandForm
from .mixins import TemplateMixin
from .models import Templates, Contracts, TemplateTypeEnum
from .services.application.use_cases.generate_contract import GenerateContract

from .services.infrastructure.converters.general import DataConverter
from .services.infrastructure.docx_editor.roland import RolandDocxEditor
from .services.infrastructure.docx_editor.royal import RoyalDocxEditor
from .services.infrastructure.formatters.roland import RolandFormatter
from .services.infrastructure.formatters.royal import RoyalFormatter


class ContractTemplatesSearchFormView(BusinessEntityMixin, TemplateMixin, ListView):
    model = Templates
    template_name = 'contract_templates/partials/forms/_search.html'
    context_object_name = 'templates'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.all()
        queryset = self.filter_by_business_entity(self.business_entity, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context


class ContractTemplatesSearchView(BusinessEntityMixin, SearchMixin, TemplateMixin, ListView):
    model = Templates
    template_name = 'contract_templates/partials/lists/_search.html'
    context_object_name = 'templates'
    paginate_by = 5
    search_param_name = 'searchTemplates'
    search_fields = [
        'name',
        'business_entity_type'
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.all()
        queryset = self.filter_by_business_entity(self.business_entity, queryset)
        queryset = self.search_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('searchTemplates', '')
        context['business_entity'] = self.business_entity
        return context


class ContractDocumentDetailListView(BusinessEntityMixin, DocumentMixin, ListView):
    model = Documents
    template_name = 'documents/detail_list.html'
    context_object_name = 'documents'
    paginate_by = 5

    def get_queryset(self):
        return self.business_entities_documents(self.business_entity)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context


class ContractDocumentDeleteView(BusinessEntityMixin, DocumentMixin, View):
    template_name = 'documents/detail_list.html'

    def post(self, request, *args, **kwargs):
        document = self.document
        contract = document.contract
        contract.delete()

        context = {
            'documents': self.business_entities_documents(self.business_entity),
            'business_entity': self.business_entity,
        }
        return render(request, self.template_name, context)


class ContractCreateView(BusinessEntityMixin, VehicleMixin, TemplateMixin, DocumentMixin, View):
    template_name = "contracts/partials/forms/_create.html"

    def get_form_class(self):
        if self.template_obj.template_type == TemplateTypeEnum.ROYAL:
            return RoyalForm
        return RolandForm

    def get_context_data(self, form):
        return {
            "time_range_form": form,
            "business_entity": self.business_entity,
            "template": self.template_obj,
            "documents": self.business_entities_documents(business_entity=self.business_entity),
        }

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class()
        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):

        converter = DataConverter()
        if self.template_obj.template_type == TemplateTypeEnum.ROYAL:
            formatter = RoyalFormatter()
            editor = RoyalDocxEditor(self.template_obj.path.path)
        else:
            formatter = RolandFormatter()
            editor = RolandDocxEditor(self.template_obj.path.path)

        generate_contract = GenerateContract(converter=converter, formatter=formatter, editor=editor)
        generate_contract.execute(
            form=form,
            contract_business_entity=self.business_entity,
            contract_vehicle_entities=self.vehicles_with_business_entity(self.business_entity),
            contract_template=self.template_obj,
        )

        context = self.get_context_data(form)

        return render(self.request, "documents/detail_list.html", context)

    def form_invalid(self, form):
        context = self.get_context_data(form)
        return render(self.request, self.template_name, context)


class ContractTemplatesListView(ListView):
    model = Templates
    template_name = 'contract_templates/list.html'
    context_object_name = 'templates'
    paginate_by = 8


class TemplateCreateView(CreateView):
    model = Templates
    form_class = TemplatesForm
    template_name = 'contract_templates/create.html'
    success_url = reverse_lazy('templates:list')
    pk_url_kwarg = 'template_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_form'] = context.pop('form', None)
        context['template'] = self.object
        return context


class TemplateUpdateView(UpdateView):
    model = Templates
    form_class = TemplatesForm
    template_name = 'contract_templates/update.html'
    success_url = reverse_lazy('templates:list')
    pk_url_kwarg = 'template_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_form'] = context.pop('form', None)
        context['template'] = self.object
        return context


class TemplatesDownloadView(DocumentMixin, View):
    def get(self, request, template_id):
        response = self.download_file(Templates, template_id)
        return response
