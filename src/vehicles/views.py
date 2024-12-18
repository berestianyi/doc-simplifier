from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, View

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
                'vehicle': vehicle,
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
