from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, UpdateView

from business_entities.models import BusinessEntities
from business_entities.views import BusinessEntityMixin
from .forms import BankDetailForm, BankCreateForm, BankUpdateForm
from .models import Bank


class BankMixin:
    @cached_property
    def bank(self):
        bank_id = self.kwargs.get("bank_id")
        return get_object_or_404(Bank, pk=bank_id)


class BankSearchCreateFormView(BusinessEntityMixin, ListView):
    model = Bank
    template_name = 'banks/partials/search_form.html'
    context_object_name = 'banks'
    paginate_by = 5

    def get_queryset(self):
        queryset = (
            Bank.objects
            .annotate(num_entities=Count('business_entities'))
            .order_by('-num_entities', 'name')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context

#
# def create_bank_search_form(request, business_entity_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#
#     banks = (
#         Bank.objects
#         .annotate(num_entities=Count('business_entities'))
#         .order_by('-num_entities', 'name')
#     )
#
#     return render(
#         request,
#         'banks/partials/search_form.html',
#         {
#             'banks': banks,
#             'business_entity': business_entity,
#         }
#     )


class BankSearchListView(BusinessEntityMixin, ListView):
    model = Bank
    template_name = 'banks/partials/search_list.html'
    context_object_name = 'banks'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('searchBanks', '')
        queryset = Bank.objects.annotate(
            num_entities=Count('business_entities')
        ).filter(
            Q(name__icontains=query) | Q(mfo__icontains=query)
        ).order_by('-num_entities', 'name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('searchBanks', '')
        context['business_entity'] = self.business_entity

        return context
# def search_banks(request, business_entity_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#     query = request.GET.get('q', '')
#
#     banks = (
#         Bank.objects
#         .annotate(num_entities=Count('business_entities'))
#         .filter(
#             Q(name__icontains=query) | Q(mfo__icontains=query)
#         )
#         .order_by('-num_entities', 'name')
#     )
#
#     return render(
#         request,
#         'banks/partials/search_list.html',
#         {
#             'banks': banks,
#             'query': query,
#             'business_entity': business_entity,
#         }
#     )


class AddBankToBusinessEntityView(BankMixin, BusinessEntityMixin, View):
    template_name = 'banks/detail.html'

    def get(self, request, *args, **kwargs):
        business_entity = self.business_entity
        bank = self.bank

        if business_entity.bank:
            business_entity.bank = None

        business_entity.bank = bank
        business_entity.save()

        bank_form = BankDetailForm(instance=bank)

        return render(request, self.template_name, {
            'bank_form': bank_form,
            'business_entity': business_entity,
        })
#
# def add_bank_to_business_entity(request, business_entity_id, bank_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#     bank = get_object_or_404(Bank, pk=bank_id)
#
#     if business_entity.bank:
#         business_entity.bank = None
#
#     business_entity.bank = bank
#     business_entity.save()
#
#     bank_form = BankDetailForm(instance=bank)
#
#     return render(
#         request,
#         'banks/detail.html',
#         {
#             'bank_form': bank_form,
#             'business_entity': business_entity,
#         }
#     )


class BankDetailView(BusinessEntityMixin, TemplateView):
    template_name = 'banks/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business_entity = self.business_entity
        bank = business_entity.bank

        if bank:
            bank_form = BankDetailForm(instance=bank)
        else:
            bank_form = ''

        context['bank_form'] = bank_form
        context['business_entity'] = business_entity
        return context
#
# def create_bank_detail_form(request, business_entity_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#     bank = business_entity.bank
#
#     if bank:
#         bank_form = BankDetailForm(instance=bank)
#     else:
#         bank_form = ''
#
#     context = {
#         'bank_form': bank_form,
#         'business_entity': business_entity,
#     }
#
#     return render(request, 'banks/detail.html', context)


class BankCreateView(BusinessEntityMixin, CreateView):
    model = Bank
    form_class = BankCreateForm
    template_name = 'banks/create.html'

    def form_valid(self, form):
        bank = form.save()
        business_entity = self.business_entity
        business_entity.bank = bank
        business_entity.save()
        return render(
            self.request,
            'banks/detail.html',
            {
                'bank_form': BankDetailForm(instance=bank),
                'business_entity': business_entity,
            }
        )

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                'bank_form': form,
                'business_entity': self.business_entity,
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context

# def create_bank_form(request, business_entity_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#     bank_form = BankCreateForm(request.POST or None)
#
#     if request.method == 'POST':
#         if bank_form.is_valid():
#             bank = bank_form.save()
#             business_entity.bank = bank
#             business_entity.save()
#
#             return render(
#                 request,
#                 'banks/detail.html',
#                 {
#                     'bank_form': BankDetailForm(instance=bank),
#                     'business_entity': business_entity,
#                 }
#             )
#
#     return render(
#         request,
#         'banks/create.html', {
#             'bank_form': bank_form,
#             'business_entity': business_entity,
#         })


class BankUpdateView(BusinessEntityMixin, UpdateView):
    model = Bank
    form_class = BankUpdateForm
    template_name = 'banks/partials/update_form.html'

    def get_object(self, queryset=None):
        business_entity = self.business_entity
        return business_entity.bank

    def form_valid(self, form):
        bank = form.save()
        business_entity = self.business_entity
        business_entity.bank = bank
        business_entity.save()

        return render(
            self.request,
            'banks/detail.html',
            {
                'bank_form': BankDetailForm(instance=bank),
                'business_entity': business_entity,
            }
        )

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                'bank_form': form,
                'business_entity': self.business_entity,
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        context['bank_form'] = BankUpdateForm(instance=self.business_entity.bank)
        return context

# def update_bank_form(request, business_entity_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#     bank_form = BankCreateForm(request.POST or None, instance=business_entity.bank)
#
#     if request.method == 'POST':
#         if bank_form.is_valid():
#             bank = bank_form.save()
#             business_entity.bank = bank
#             business_entity.save()
#
#             return render(
#                 request,
#                 'banks/detail.html',
#                 {
#                     'bank_form': BankDetailForm(instance=bank),
#                     'business_entity': business_entity,
#                 }
#             )
#
#     return render(
#         request,
#         'banks/partials/update_form.html', {
#             'bank_form': bank_form,
#             'business_entity': business_entity,
#         })


class BankDeleteView(BusinessEntityMixin, View):
    template_name = 'banks/detail.html'

    def get(self, request, *args, **kwargs):
        business_entity = self.business_entity
        business_entity.bank = None
        business_entity.save()

        return render(
            request,
            self.template_name,
            {
                'bank_form': '',
                'business_entity': business_entity,
            }
        )

# def delete_bank(request, business_entity_id):
#     business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
#     business_entity.bank = None
#     business_entity.save()
#
#     return render(request, 'banks/detail.html', {
#         'bank_form': '',
#         'business_entity': business_entity,
#     })
