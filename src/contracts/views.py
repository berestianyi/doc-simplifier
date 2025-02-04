import os
from django.http import Http404, FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, UpdateView

from business_entities.mixins import SearchMixin
from business_entities.views import BusinessEntityMixin
from documents.mixins import DocumentMixin
from documents.models import Documents
from vehicles.mixins import VehicleMixin
from .forms import ContractTimeRangeForm, TemplatesForm
from .mixins import TemplateMixin
from .models import Templates, Contracts
from .services import WordDocManager


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


class ContractCreateView(BusinessEntityMixin, VehicleMixin, TemplateMixin, DocumentMixin, CreateView):
    template_name = "contracts/partials/forms/_create.html"
    model = Contracts
    form_class = ContractTimeRangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_range_form'] = context.pop('form', None)
        context['business_entity'] = self.business_entity
        context['template'] = self.template_obj
        return context

    def form_valid(self, form, *args, **kwargs):
        contract = form.save(commit=False)
        contract.business_entities = self.business_entity
        contract.template = self.template_obj
        contract.save()

        start_date = form.cleaned_data["start_date"]
        expire_date = form.cleaned_data["end_date"]
        vehicles_with_entities = self.vehicles_with_business_entity(business_entity=self.business_entity)

        replacement_manager = self.get_replacement_manager_class()(
            start_date=start_date,
            expire_date=expire_date,
            business_entity=self.business_entity,
            bank=self.business_entity.bank,
            vehicles=vehicles_with_entities,
        )

        word_manager = WordDocManager(template_path=self.template_obj.path.path)

        replacement_dict = replacement_manager.replacements_generator()
        cars_dict = replacement_manager.cars_info_generator()

        word_manager.replace_placeholders(replacement_dict)
        word_manager.add_car_info_to_table(cars_dict)

        filename = word_manager.create_output_filename(
            self.template_obj,
            self.business_entity,
            contract.id
        )
        output = word_manager.save_word_file(filename=filename)
        Documents.objects.create(
            name=filename,
            path=output,
            contract=contract
        )

        documents = self.business_entities_documents(business_entity=self.business_entity)

        context = {
            "time_range_form": form,
            "business_entity": self.business_entity,
            "template": self.template_obj,
            "documents": documents,
        }
        return render(self.request, "documents/detail_list.html", context)

    def form_invalid(self, form, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     context['time_range_form'] = ContractTimeRangeForm()
    #     context['business_entity'] = self.business_entity
    #     context['template'] = self.template_obj
    #     return self.render_to_response(context)
    #
    # def post(self, request, *args, **kwargs):
    #     time_range_form = ContractTimeRangeForm(request.POST)
    #     if time_range_form.is_valid():
    #         vehicles_with_entities = self.vehicles_with_business_entity(business_entity=self.business_entity)
    #
    #         start_date = time_range_form.cleaned_data["start_date"]
    #         expire_date = time_range_form.cleaned_data["end_date"]
    #
    #         contract = Contracts.objects.create(
    #             business_entities=self.business_entity,
    #             template=self.template_obj,
    #             start_date=start_date,
    #             end_date=expire_date,
    #         )
    #         contract.save()
    #
    #         replacement_manager = self.get_replacement_manager_class()(
    #                 start_date=start_date,
    #                 expire_date=expire_date,
    #                 business_entity=self.business_entity,
    #                 bank=self.business_entity.bank,
    #                 vehicles=vehicles_with_entities,
    #             )
    #
    #         word_manager = WordDocManager(template_path=self.template_obj.path.path)
    #
    #         replacement_dict = replacement_manager.replacements_generator()
    #         cars_dict = replacement_manager.cars_info_generator()
    #
    #         word_manager.replace_placeholders(replacement_dict)
    #         word_manager.add_car_info_to_table(cars_dict)
    #
    #         filename = word_manager.create_output_filename(
    #             self.template_obj,
    #             self.business_entity,
    #             contract.id
    #         )
    #         output = word_manager.save_word_file(filename=filename)
    #
    #         document_entity = Documents.objects.create(
    #             name=filename,
    #             path=output,
    #             contract=contract
    #         )
    #         document_entity.save()
    #         documents = Documents.objects.filter(contract__business_entities=self.business_entity)
    #
    #         context = {
    #             "time_range_form": time_range_form,
    #             "business_entity": self.business_entity,
    #             "template": self.template_obj,
    #             "documents": documents,
    #         }
    #         return render(request, "documents/_detail.html", context)
    #
    #     context = self.get_context_data(**kwargs)
    #     context['time_range_form'] = time_range_form
    #     return self.render_to_response(context)
    #


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
