from django.shortcuts import render, redirect

from business_entities.forms import BusinessEntitiesForm
from business_entities.models import BusinessEntities


def home_page(request):
    return render(request, 'base.html')


def business_entities(request):
    return render(request, 'business_entity/list.html')


def business_entity(request):
    return render(request, 'business_entity/page.html')


def create_business_entity(request):
    if request.method == 'POST':
        data = request.POST
        edrpou = data.get('edrpou', '').strip()
        form = BusinessEntitiesForm(request.POST, request.FILES)
        if form.is_valid():
            if len(edrpou) == 8:
                business_entity_type = BusinessEntities.BusinessEntitiesEnum.FOP
                short_name = full_name = director_name = data.get('fop_name', '')
            elif len(edrpou) == 10:
                business_entity_type = BusinessEntities.BusinessEntitiesEnum.TOV
                short_name = full_name = data.get('company_name', '')
                director_name = data.get('director_name', '')
            else:
                return render(request, 'business_entity/create.html', {'error': 'Неправильний код ЕДРПОУ'})

            business_entity_instance = BusinessEntities(
                business_entity=business_entity_type,
                edrpou=edrpou,
                short_name=short_name,
                full_name=full_name,
                director_name=director_name,
                address=data.get('address', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                iban=data.get('iban', ''),
            )

            business_entity_instance.save()
            return redirect('business_entities')
    else:
        form = BusinessEntitiesForm()

    return render(
        request,
        'business_entity/create.html',
        {'form': form}
    )

