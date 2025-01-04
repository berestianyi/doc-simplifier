from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404

from business_entities.models import BusinessEntities
from .forms import BankDetailForm, BankCreateForm
from .models import Bank


def create_bank_search_form(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)

    banks = (
        Bank.objects
        .annotate(num_entities=Count('business_entities'))
        .order_by('-num_entities', 'name')
    )

    return render(
        request,
        'banks/partials/bank_search_form.html',
        {
            'banks': banks,
            'business_entity': business_entity,
        }
    )


def search_banks(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    query = request.GET.get('q', '')

    banks = (
        Bank.objects
        .annotate(num_entities=Count('business_entities'))
        .filter(
            Q(name__icontains=query) | Q(mfo__icontains=query)
        )
        .order_by('-num_entities', 'name')
    )

    return render(
        request,
        'banks/partials/bank_search_list.html',
        {
            'banks': banks,
            'query': query,
            'business_entity': business_entity,
        }
    )


def add_bank_to_business_entity(request, business_entity_id, bank_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    bank = get_object_or_404(Bank, pk=bank_id)

    if business_entity.bank:
        business_entity.bank = None

    business_entity.bank = bank
    business_entity.save()

    bank_form = BankDetailForm(instance=bank)

    return render(
        request,
        'banks/detail.html',
        {
            'bank_form': bank_form,
            'business_entity': business_entity,
        }
    )


def create_bank_detail_form(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    bank = business_entity.bank

    if bank:
        bank_form = BankDetailForm(instance=bank)
    else:
        bank_form = ''

    context = {
        'bank_form': bank_form,
        'business_entity': business_entity,
    }

    return render(request, 'banks/detail.html', context)


def create_bank_form(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    bank_form = BankCreateForm(request.POST or None)

    if request.method == 'POST':
        if bank_form.is_valid():
            bank = bank_form.save()
            business_entity.bank = bank
            business_entity.save()

            return render(
                request,
                'banks/detail.html',
                {
                    'bank_form': BankDetailForm(instance=bank),
                    'business_entity': business_entity,
                }
            )

    return render(
        request,
        'banks/create.html', {
            'bank_form': bank_form,
            'business_entity': business_entity,
        })


def update_bank_form(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    bank_form = BankCreateForm(request.POST or None, instance=business_entity.bank)

    if request.method == 'POST':
        if bank_form.is_valid():
            bank = bank_form.save()
            business_entity.bank = bank
            business_entity.save()

            return render(
                request,
                'banks/detail.html',
                {
                    'bank_form': BankDetailForm(instance=bank),
                    'business_entity': business_entity,
                }
            )

    return render(
        request,
        'banks/partials/update_form.html', {
            'bank_form': bank_form,
            'business_entity': business_entity,
        })


def delete_bank(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    business_entity.bank = None
    business_entity.save()

    return render(request, 'banks/detail.html', {
        'bank_form': '',
        'business_entity': business_entity,
    })
