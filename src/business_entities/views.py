from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from banks.forms import BankDetailForm
from contracts.models import Contracts
from .forms import FOPCreateForm, TOVCreateForm, FOPDetailForm, TOVDetailForm, TOVUpdateForm, \
    FOPUpdateForm
from .models import BusinessEntities
from vehicles.models import Vehicles


def business_entities_list(request):
    business_entities = BusinessEntities.objects.all()
    business_entities_choices = BusinessEntities.BusinessEntitiesEnum

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
            fop.business_entity = BusinessEntities.BusinessEntitiesEnum.FOP
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
            tov.business_entity = BusinessEntities.BusinessEntitiesEnum.TOV
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
    contracts = Contracts.objects.filter(business_entities_id=business_entity_id)

    context = {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
        'vehicles_with_entities': vehicles_with_entities,
        'bank_form': bank_form,
        'contracts': contracts,
    }
    return render(request, 'business_entities/detail.html', context)


def business_entity_detail_form(request, business_entity_id):
    business_entity = BusinessEntities.objects.get(pk=business_entity_id)
    if business_entity.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
        business_entity_form = FOPDetailForm(instance=business_entity)
    else:
        business_entity_form = TOVDetailForm(instance=business_entity)

    return render(request, 'business_entities/partials/update_and_detail_form.html', {
        'business_entity_form': business_entity_form,
        'business_entity': business_entity,
    })


def business_entity_update_form(request, business_entity_id):
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
