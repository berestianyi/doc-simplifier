from typing import List
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, View

from business_entities.models import BusinessEntities
from business_entities.views import HtmxTemplateMixin, SortOrderMixin, SearchMixin, BusinessEntityMixin
from .forms import (
    VehiclesCreateForm,
    VehiclesUpdateForm,
    VehicleLicencesUpdateForm,
    VehiclesDetailForm,
    VehicleLicencesDetailForm,
    VehicleLicencesCreateForm
)
from vehicles.models import Vehicles, VehicleLicences


class VehicleMixin:

    @classmethod
    def get_vehicle_and_licence_objects(cls, vehicle_id):
        vehicle = get_object_or_404(Vehicles, id=vehicle_id)
        licence = get_object_or_404(VehicleLicences, vehicle=vehicle)
        return vehicle, licence

    @classmethod
    def vehicles_without_business_entities(cls, business_entity):
        owned_vehicle_ids = VehicleLicences.objects.filter(
            business_entities=business_entity
        ).values_list('vehicle_id', flat=True)
        unowned_vehicles = Vehicles.objects.exclude(id__in=owned_vehicle_ids)

        return unowned_vehicles

    @classmethod
    def vehicles_with_business_entity(cls, business_entity: BusinessEntities):
        return Vehicles.objects.filter(vehiclelicences__business_entities=business_entity).distinct()


class VehiclesListView(HtmxTemplateMixin, SortOrderMixin, SearchMixin, ListView):
    model = Vehicles
    template_name = 'vehicles/list.html'
    htmx_template_name = 'vehicles/partials/list_fields.html'
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


class CreateVehicleView(View):
    template_name = 'vehicles/CRUD.html'

    def get(self, request, *args, **kwargs):
        vehicle_form = VehiclesCreateForm()
        licence_form = VehicleLicencesCreateForm()
        return render(
            request,
            self.template_name,
            {
                'vehicle_form': vehicle_form,
                'licence_form': licence_form,
                'action': 'create'
            }
        )

    def post(self, request, *args, **kwargs):
        vehicle_form = VehiclesCreateForm(request.POST)
        licence_form = VehicleLicencesCreateForm(request.POST)

        if vehicle_form.is_valid() and licence_form.is_valid():
            vehicle = vehicle_form.save(commit=True)
            licence = licence_form.save(commit=False)
            licence.vehicle = vehicle
            licence.save()
            return redirect('vehicles:detail', vehicle_id=vehicle.id)

        return render(
            request,
            self.template_name,
            {
                'vehicle_form': vehicle_form,
                'licence_form': licence_form,
                'action': 'create'
            }
        )


class VehicleAndLicenceDetailView(VehicleMixin, HtmxTemplateMixin, View):
    template_name = 'vehicles/CRUD.html'
    htmx_template_name = 'vehicles/partials/CRUD_form.html'

    def get(self, request, vehicle_id):
        vehicle, licence = self.get_vehicle_and_licence_objects(vehicle_id)

        context = {
            'vehicle_form': VehiclesDetailForm(instance=vehicle),
            'licence_form': VehicleLicencesDetailForm(instance=licence),
            'vehicle': vehicle,
            'licence': licence,
            'action': 'detail'
        }
        templates = self.get_template_names()
        selected_template = templates[0] if templates else self.template_name

        return render(request, selected_template, context)


class VehicleAndLicenceUpdateView(VehicleMixin, View):
    template_name = 'vehicles/partials/CRUD_form.html'

    def get(self, request, vehicle_id):
        vehicle, licence = self.get_vehicle_and_licence_objects(vehicle_id)
        context = {
            'vehicle_form': VehiclesUpdateForm(instance=vehicle),
            'licence_form': VehicleLicencesUpdateForm(instance=licence),
            'vehicle': vehicle,
            'action': 'update'
        }
        return render(request, self.template_name, context)

    def post(self, request, vehicle_id):
        vehicle, licence = self.get_vehicle_and_licence_objects(vehicle_id)
        licence_update_form = VehicleLicencesUpdateForm(request.POST, instance=licence)
        vehicle_update_form = VehiclesUpdateForm(request.POST, instance=vehicle)

        if licence_update_form.is_valid() and vehicle_update_form.is_valid():
            updated_licence = licence_update_form.save()
            updated_vehicle = vehicle_update_form.save()
            return render(request, self.template_name, {
                'licence_form': VehicleLicencesDetailForm(instance=updated_licence),
                'vehicle_form': VehiclesDetailForm(instance=updated_vehicle),
                'vehicle': updated_vehicle,
                'action': 'detail'
            })
        else:
            return render(request, self.template_name, {
                'licence_form': licence_update_form,
                'vehicle_form': vehicle_update_form,
                'vehicle': vehicle,
                'action': 'update'
            })


class VehicleAndLicenceDeleteView(VehicleMixin, View):
    def post(self, request, vehicle_id):
        vehicle, licence = self.get_vehicle_and_licence_objects(vehicle_id)
        vehicle.delete()
        licence.delete()
        response = HttpResponse("")
        redirect_url = reverse("vehicles:list")
        response["HX-Redirect"] = redirect_url
        return response


class VehicleRedirectToDetailView(View):
    def get(self, request, vehicle_id, *args, **kwargs):
        response = HttpResponse("")
        redirect_url = reverse("vehicles:detail", kwargs={'vehicle_id': vehicle_id})
        response["HX-Redirect"] = redirect_url
        return response


class VehicleRedirectToCreateView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse("")
        redirect_url = reverse("vehicles:create")
        response["HX-Redirect"] = redirect_url
        return response


class CreateSearchVehicleFormView(BusinessEntityMixin, VehicleMixin, ListView):
    template_name = 'vehicles/partials/search_form.html'
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
    template_name = 'vehicles/partials/search_list.html'
    context_object_name = 'vehicles_without_entities'
    paginate_by = 5
    search_param_name = 'searchVehicles'
    search_fields: List[str] = ['number']

    def get_queryset(self):
        queryset = self.vehicles_without_business_entities(self.business_entity)
        queryset = self.search_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        context['query'] = self.get_search_query()

        return context


class AddVehicleToBusinessEntityView(VehicleMixin, View):
    template_name = 'vehicles/detail_list.html'

    def post(self, request, business_entity_id, vehicle_id, *args, **kwargs):
        business_entity = get_object_or_404(BusinessEntities, id=business_entity_id)
        vehicle, licence = self.get_vehicle_and_licence_objects(vehicle_id)

        licence.business_entities.add(business_entity)
        licence.save()

        vehicles_with_entities = self.vehicles_with_business_entity(business_entity)

        context = {
            'vehicles_with_entities': vehicles_with_entities,
            'business_entity': business_entity,
        }
        return render(request, self.template_name, context)


class RemoveVehicleFromBusinessEntityView(VehicleMixin, View):
    template_name = 'vehicles/detail_list.html'

    def post(self, request, business_entity_id, vehicle_id, *args, **kwargs):
        business_entity = get_object_or_404(BusinessEntities, id=business_entity_id)
        vehicle, licence = self.get_vehicle_and_licence_objects(vehicle_id)

        licence.business_entities.remove(business_entity)
        licence.save()

        vehicles_with_entities = self.vehicles_with_business_entity(business_entity)

        context = {
            'vehicles_with_entities': vehicles_with_entities,
            'business_entity': business_entity,
        }
        return render(request, self.template_name, context)


class VehiclesInBusinessEntityListView(VehicleMixin, ListView):
    model = Vehicles
    template_name = 'vehicles/detail_list.html'
    context_object_name = 'vehicles_with_entities'

    def get_queryset(self):
        business_entity_id = self.kwargs['business_entity_id']
        business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
        return self.vehicles_with_business_entity(business_entity)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business_entity_id = self.kwargs['business_entity_id']
        context['business_entity'] = get_object_or_404(BusinessEntities, pk=business_entity_id)
        return context


class VehiclesInBusinessEntityView(VehicleMixin, View):
    template_name = 'vehicles/detail_list.html'

    def get(self, request, business_entity_id, *args, **kwargs):
        business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
        vehicles_with_entities = self.vehicles_with_business_entity(business_entity)

        context = {
            'vehicles_with_entities': vehicles_with_entities,
            'business_entity': business_entity,
        }
        return render(request, self.template_name, context)
