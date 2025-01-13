from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, View

from business_entities.models import BusinessEntities
from .forms import (
    VehiclesCreateForm,
    VehiclesUpdateForm,
    VehicleLicencesUpdateForm,
    VehiclesDetailForm,
    VehicleLicencesDetailForm,
    VehicleLicencesCreateForm
)
from vehicles.models import Vehicles, VehicleLicences


class VehiclesListView(ListView):
    model = Vehicles
    template_name = 'vehicles/list.html'
    context_object_name = 'vehicles'
    paginate_by = 10


class CreateVehicleView(View):
    template_name = 'vehicles/create.html'

    def get(self, request, *args, **kwargs):
        vehicle_form = VehiclesCreateForm()
        licence_form = VehicleLicencesCreateForm()
        return render(
            request,
            self.template_name,
            {
                'vehicle_form': vehicle_form,
                'licence_form': licence_form
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

            return redirect('vehicle_detail', vehicle_id=vehicle.id)

        return render(
            request,
            self.template_name,
            {
                'vehicle_form': vehicle_form,
                'licence_form': licence_form
            }
        )


def get_vehicle_and_licence_objects(vehicle_id):
    vehicle = get_object_or_404(Vehicles, id=vehicle_id)
    licence = get_object_or_404(VehicleLicences, vehicle=vehicle)
    return vehicle, licence


def vehicles_detail(request, vehicle_id):
    vehicle, licence = get_vehicle_and_licence_objects(vehicle_id)

    context = {
        'vehicle_form': VehiclesDetailForm(instance=vehicle),
        'licence_form': VehicleLicencesDetailForm(instance=licence),
        'vehicle': vehicle,
        'licence': licence
    }
    return render(request, 'vehicles/detail.html', context)


def create_vehicle_and_licence_update_form(request, vehicle_id):
    vehicle, licence = get_vehicle_and_licence_objects(vehicle_id)
    context = {
        'vehicle_form': VehiclesUpdateForm(instance=vehicle),
        'licence_form': VehicleLicencesUpdateForm(instance=licence),
        'vehicle': vehicle,
    }
    return render(request, 'vehicles/partials/update_form.html', context)


def submit_vehicle_and_licence_update_form(request, vehicle_id):
    vehicle, licence = get_vehicle_and_licence_objects(vehicle_id)
    licence_update_form = VehicleLicencesUpdateForm(request.POST or None, instance=licence)
    vehicle_update_form = VehiclesUpdateForm(request.POST or None, instance=vehicle)

    if request.method == 'POST':
        if licence_update_form.is_valid() and vehicle_update_form.is_valid():
            updated_licence = licence_update_form.save()
            updated_vehicle = vehicle_update_form.save()

            return render(request, 'vehicles/partials/detail_form.html', {
                'licence_form': VehicleLicencesDetailForm(instance=updated_licence),
                'vehicle_form': VehiclesDetailForm(instance=updated_vehicle),
                'vehicle': updated_vehicle,
            })
        else:
            return render(request, 'vehicles/partials/update_form.html', {
                'licence_form': licence_update_form,
                'vehicle_form': vehicle_update_form,
                'vehicle': vehicle,
            })

    return render(request, 'vehicles/partials/update_form.html', {
        'licence_form': licence_update_form,
        'vehicle_form': vehicle_update_form,
        'vehicle': vehicle,
    })


def delete_vehicle_and_licence(request, vehicle_id):
    vehicle, licence = get_vehicle_and_licence_objects(vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        licence.delete()
        response = HttpResponse("")
        redirect_url = reverse("vehicles")
        response["HX-Redirect"] = redirect_url
        return response


def redirect_to_vehicle_detail(request, vehicle_id):
    response = HttpResponse("")
    redirect_url = reverse("vehicle_detail", kwargs={'vehicle_id': vehicle_id})
    response["HX-Redirect"] = redirect_url
    return response


def redirect_to_vehicle_create_form(request):
    response = HttpResponse("")
    redirect_url = reverse("create_vehicle")
    response["HX-Redirect"] = redirect_url
    return response


def create_search_vehicle_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    vehicles_without_entities = (
        Vehicles.objects
        .annotate(num_entities=Count('vehiclelicences__business_entities'))
        .filter(num_entities=0)
    )

    return render(
        request,
        'vehicles/partials/vehicle_search_form.html',
        {
            'vehicles_without_entities': vehicles_without_entities,
            'business_entity': business_entity
        }
    )


def search_vehicles_without_entities(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    query = request.GET.get('q', '')

    vehicles_without_entities = (
        Vehicles.objects
        .annotate(num_entities=Count('vehiclelicences__business_entities'))
        .filter(num_entities=0)
    )

    if query:
        vehicles_without_entities = vehicles_without_entities.filter(
            number__icontains=query
        )

    return render(
        request,
        'vehicles/templates/vehicles/partials/vehicle_search_list.html',
        {
            'vehicles_without_entities': vehicles_without_entities,
            'query': query,
            'business_entity': business_entity,
        }
    )


def add_vehicle_to_business_entity(request, business_entity_id, vehicle_id):
    business_entity = get_object_or_404(BusinessEntities, id=business_entity_id)
    vehicle = get_object_or_404(Vehicles, id=vehicle_id)
    vehicle_licence = get_object_or_404(VehicleLicences, vehicle=vehicle)
    vehicle_licence.business_entities.add(business_entity)
    vehicle_licence.save()

    vehicles_with_entities = (
        Vehicles.objects
        .filter(vehiclelicences__business_entities=business_entity)
        .distinct()
    )

    context = {
        'vehicles_with_entities': vehicles_with_entities,
        'business_entity': business_entity,
    }

    return render(request, 'business_entities/../vehicles/templates/vehicles/vehicle_list.html', context)


def remove_vehicle_from_business_entity(request, business_entity_id, vehicle_id):
    business_entity = get_object_or_404(BusinessEntities, id=business_entity_id)
    vehicle = get_object_or_404(Vehicles, id=vehicle_id)
    vehicle_licence = get_object_or_404(VehicleLicences, vehicle=vehicle)
    vehicle_licence.business_entities.remove(business_entity)
    vehicle_licence.save()

    vehicles_with_entities = (
        Vehicles.objects
        .filter(vehiclelicences__business_entities=business_entity)
        .distinct()
    )
    context = {
        'vehicles_with_entities': vehicles_with_entities,
        'business_entity': business_entity,

    }

    return render(request, 'business_entities/../vehicles/templates/vehicles/vehicle_list.html', context)


def vehicles_in_business_entity(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    vehicles_with_entities = (
        Vehicles.objects
        .filter(vehiclelicences__business_entities=business_entity)
        .distinct()
    )
    context = {
        'vehicles_with_entities': vehicles_with_entities,
        'business_entity': business_entity,
    }
    return render(request, 'business_entities/../vehicles/templates/vehicles/vehicle_list.html', context)
