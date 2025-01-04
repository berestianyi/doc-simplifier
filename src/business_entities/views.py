from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from banks.forms import BankDetailForm
from .forms import FOPCreateForm, TOVCreateForm, FOPDetailForm, TOVDetailForm, TOVUpdateForm, \
    FOPUpdateForm
from .models import BusinessEntities
from vehicles.models import Vehicles, VehicleLicences


class BusinessEntitiesListView(ListView):
    model = BusinessEntities
    template_name = 'business_entities/list.html'
    context_object_name = 'business_entities'
    paginate_by = 10


def create_business_entity(request):
    business_entity_form = FOPCreateForm()
    return render(
        request,
        'business_entities/create.html',
        {'business_entity_form': business_entity_form}
    )


def create_fop_form(request):
    business_entity_form = FOPCreateForm()
    return render(
        request,
        'business_entities/partials/create_fop_form.html',
        {'business_entity_form': business_entity_form}
    )


def submit_fop_form(request):
    fop_form = FOPCreateForm(request.POST or None)

    if fop_form.is_valid():
        fop = fop_form.save(commit=False)
        fop.business_entity = BusinessEntities.BusinessEntitiesEnum.FOP
        fop.save()

        response = HttpResponse("")
        redirect_url = reverse("business_entity_detail", kwargs={"business_entity_id": fop.id})
        response["HX-Redirect"] = redirect_url
        return response

    return render(
        request,
        'business_entities/partials/create_fop_form.html',
        {'business_entity_form': fop_form}
    )


def create_tov_form(request):
    business_entity_form = TOVCreateForm()
    return render(
        request,
        'business_entities/partials/create_tov_form.html',
        {'business_entity_form': business_entity_form}
    )


def submit_tov_form(request):
    tov_form = TOVCreateForm(request.POST or None)

    if tov_form.is_valid():
        tov = tov_form.save(commit=False)
        tov.business_entity = BusinessEntities.BusinessEntitiesEnum.TOV
        tov.save()

        response = HttpResponse("")
        redirect_url = reverse("business_entity_detail", kwargs={"business_entity_id": tov.id})
        response["HX-Redirect"] = redirect_url
        return response

    return render(
        request,
        'business_entities/partials/create_tov_form.html',
        {'business_entity_form': tov_form}
    )


def business_entity_detail(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
        business_entity_form = FOPDetailForm(instance=business_entity)
    else:
        business_entity_form = TOVDetailForm(instance=business_entity)

    bank_form = BankDetailForm(instance=business_entity.bank) if business_entity.bank else None

    vehicles_with_entities = (
        Vehicles.objects
        .filter(vehiclelicences__business_entities=business_entity)
        .distinct()
    )

    context = {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
        'vehicles_with_entities': vehicles_with_entities,
        'bank_form': bank_form,
    }
    return render(request, 'business_entities/detail.html', context)


def create_business_entity_detail_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
        business_entity_form = FOPDetailForm(instance=business_entity)
    else:
        business_entity_form = TOVDetailForm(instance=business_entity)

    context = {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
    }

    return render(request, 'business_entities/partials/detail_form.html', context)


def create_business_entity_update_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
        business_entity_form = FOPUpdateForm(instance=business_entity)
    else:
        business_entity_form = TOVUpdateForm(instance=business_entity)

    context = {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
    }

    return render(request, 'business_entities/partials/update_form.html', context)


def submit_business_entity_update_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
        business_entity_form = FOPUpdateForm(request.POST or None, instance=business_entity)
    else:
        business_entity_form = TOVUpdateForm(request.POST or None, instance=business_entity)

    if request.method == 'POST':
        if business_entity_form.is_valid():
            updated_business_entity = business_entity_form.save()
            if business_entity.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
                updated_business_entity_form = FOPDetailForm(instance=updated_business_entity)
            else:
                updated_business_entity_form = TOVDetailForm(instance=updated_business_entity)
            return render(request, 'business_entities/partials/detail_form.html', {
                'business_entity_form': updated_business_entity_form,
                'business_entity': updated_business_entity,
            })
        else:
            return render(request, 'business_entities/partials/update_form.html', {
                'business_entity_form': business_entity_form,
                'business_entity': business_entity,
            })

    return render(request, 'business_entities/partials/update_form.html', {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
    })


def delete_business_entity(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if request.method == 'POST':
        business_entity.delete()
        response = HttpResponse("")
        redirect_url = reverse("business_entities")
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
        'business_entities/partials/vehicle_search_form.html',
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
        'business_entities/partials/vehicle_search_list.html',
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

    return render(request, 'business_entities/vehicle_list.html', context)


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

    return render(request, 'business_entities/vehicle_list.html', context)


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
    return render(request, 'business_entities/vehicle_list.html', context)
