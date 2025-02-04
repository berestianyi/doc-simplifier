from typing import List
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View, CreateView, TemplateView, UpdateView

from business_entities.mixins import HtmxMixin, SearchMixin, SortOrderMixin, BusinessEntityMixin
from .forms import (
    VehiclesCreateForm,
    VehiclesUpdateForm,
    VehicleLicencesUpdateForm,
    VehiclesDetailForm,
    VehicleLicencesDetailForm,
    VehicleLicencesCreateForm
)
from .models import Vehicles
from .mixins import VehicleMixin


class VehiclesListView(HtmxMixin, SortOrderMixin, SearchMixin, ListView):
    model = Vehicles
    template_name = 'vehicles/list.html'
    htmx_template_name = 'vehicles/partials/_fields.html'
    context_object_name = 'vehicles'
    paginate_by = 10
    search_param_name = 'searchVehicles'
    search_fields = [
        'vin_code',
        'vehicle_type',
        'number',
        'brand',
        'model',
        'year',
        'unladen_weight',
        'laden_weight',
        'engine_capacity',
        'number_of_seats',
        'euro',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.search_queryset(queryset)
        queryset = self.sort_queryset(queryset)
        return queryset


class CreateVehicleView(BusinessEntityMixin, CreateView):
    model = Vehicles
    form_class = VehiclesCreateForm
    template_name = 'vehicles/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_form'] = context.pop('form', None)
        if 'licence_form' not in context:
            context['licence_form'] = VehicleLicencesCreateForm(self.request.POST or None)
        context['business_entity'] = self.business_entity
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        vehicle_form = context.get('vehicle_form')
        licence_form = context.get('licence_form')
        if licence_form.is_valid():
            self.object = vehicle_form.save()
            licence = licence_form.save(commit=False)
            licence.vehicle = self.object
            licence.save()
            if self.business_entity:
                licence.business_entities.add(self.business_entity)
                licence.save()
                return redirect(
                    'business_entities:detail',
                    business_entity_id=self.business_entity.id
                )
            return redirect('vehicles:detail', vehicle_id=self.object.id)
        else:
            return self.form_invalid(vehicle_form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class VehicleAndLicenceDetailView(VehicleMixin, HtmxMixin, TemplateView):
    template_name = 'vehicles/detail.html'
    htmx_template_name = 'vehicles/partials/forms/_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'vehicle_form': VehiclesDetailForm(instance=self.vehicle),
            'licence_form': VehicleLicencesDetailForm(instance=self.vehicle_licence),
            'vehicle': self.vehicle,
            'licence': self.vehicle_licence,
        })
        return context


class VehicleAndLicenceUpdateView(VehicleMixin, UpdateView):
    model = Vehicles
    form_class = VehiclesUpdateForm
    template_name = 'vehicles/partials/forms/_update.html'
    detail_template_name = 'vehicles/partials/forms/_detail.html'

    def get_object(self, queryset=None):
        return self.vehicle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_form'] = context.pop('form', None)
        context['licence_form'] = VehicleLicencesUpdateForm(
            self.request.POST or None,
            instance=self.vehicle_licence
        )
        context['vehicle'] = self.vehicle
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        vehicle_form = context.get('vehicle_form')
        licence_form = context.get('licence_form')

        if licence_form.is_valid():
            updated_vehicle = vehicle_form.save()
            updated_licence = licence_form.save()
            context = {
                'vehicle_form': VehiclesDetailForm(instance=updated_vehicle),
                'licence_form': VehicleLicencesDetailForm(instance=updated_licence),
                'vehicle': updated_vehicle,
            }
            return render(self.request, self.detail_template_name, context)
        else:
            return self.form_invalid(vehicle_form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class VehicleAndLicenceDeleteView(BusinessEntityMixin, VehicleMixin, View):
    def post(self, request,  *args, **kwargs):
        self.vehicle_licence.delete()
        return redirect('vehicles:list')


class VehicleRedirectToDetailView(HtmxMixin, View):
    def get(self, request, vehicle_id, *args, **kwargs):
        response = self.htmx_redirect("vehicles:detail", kwargs={'vehicle_id': vehicle_id})
        return response


class CreateSearchVehicleFormView(BusinessEntityMixin, VehicleMixin, ListView):
    template_name = 'vehicles/partials/forms/_search.html'
    context_object_name = 'vehicles_without_entities'
    paginate_by = 5

    def get_queryset(self):
        queryset = self.vehicles_without_business_entities(self.business_entity)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context


class SearchVehiclesWithoutEntitiesListView(VehicleMixin, BusinessEntityMixin, SearchMixin, ListView):
    model = Vehicles
    template_name = 'vehicles/partials/lists/_search.html'
    context_object_name = 'vehicles_without_entities'
    paginate_by = 5
    search_param_name = 'searchVehicles'
    search_fields: List[str] = ['number', 'model', 'brand']

    def get_queryset(self):
        queryset = self.vehicles_without_business_entities(self.business_entity)
        queryset = self.search_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        context['query'] = self.get_search_query()

        return context


class AddVehicleToBusinessEntityView(BusinessEntityMixin, VehicleMixin, View):
    template_name = 'vehicles/partials/lists/_detail.html'

    def post(self, request, *args, **kwargs):
        self.vehicle_licence.business_entities.add(self.business_entity)
        self.vehicle_licence.save()

        vehicles_with_entities = self.vehicles_with_business_entity(self.business_entity)

        context = {
            'vehicles_with_entities': vehicles_with_entities,
            'business_entity': self.business_entity,
        }
        return render(request, self.template_name, context)


class RemoveVehicleFromBusinessEntityView(BusinessEntityMixin, VehicleMixin, View):
    template_name = 'vehicles/partials/lists/_detail.html'

    def post(self, request, *args, **kwargs):
        self.vehicle_licence.business_entities.remove(self.business_entity)
        self.vehicle_licence.save()

        vehicles_with_entities = self.vehicles_with_business_entity(self.business_entity)

        context = {
            'vehicles_with_entities': vehicles_with_entities,
            'business_entity': self.business_entity,
        }
        return render(request, self.template_name, context)


class VehiclesInBusinessEntityListView(BusinessEntityMixin, VehicleMixin, ListView):
    model = Vehicles
    template_name = 'vehicles/partials/lists/_detail.html'
    context_object_name = 'vehicles_with_entities'

    def get_queryset(self):
        return self.vehicles_with_business_entity(self.business_entity)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context


class VehiclesInBusinessEntityView(BusinessEntityMixin, VehicleMixin, TemplateView):
    template_name = 'vehicles/partials/lists/_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        context['vehicles_with_entities'] = self.vehicles_with_business_entity(self.business_entity)
        return context
