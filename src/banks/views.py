from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, UpdateView

from business_entities.mixins import BusinessEntityMixin, SearchMixin

from .forms import BankDetailForm, BankCreateForm, BankUpdateForm
from .mixins import BankMixin
from .models import Bank


class BankSearchCreateFormView(BusinessEntityMixin, BankMixin, ListView):
    model = Bank
    template_name = 'banks/partials/forms/_search.html'
    context_object_name = 'banks'
    paginate_by = 5

    def get_queryset(self):
        return self.available_banks()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        return context


class BankSearchListView(BusinessEntityMixin, SearchMixin, BankMixin, ListView):
    model = Bank
    template_name = 'banks/partials/lists/_search.html'
    context_object_name = 'banks'
    search_param_name = 'searchBanks'
    search_fields = ['name', 'mfo']
    paginate_by = 5

    def get_queryset(self):
        queryset = self.available_banks()
        queryset = self.search_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.get_queryset()
        context['business_entity'] = self.business_entity
        return context


class AddBankToBusinessEntityView(BankMixin, BusinessEntityMixin, View):
    template_name = 'banks/detail.html'

    def post(self, request, *args, **kwargs):
        business_entity = self.business_entity
        bank = self.bank

        if business_entity.bank:
            business_entity.bank = None

        business_entity.bank = bank
        business_entity.save()

        context = {
            'bank_form': BankDetailForm(instance=bank),
            'business_entity': business_entity,
        }

        return render(request, self.template_name, context)


class BankDetailView(BusinessEntityMixin, TemplateView):
    template_name = 'banks/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business_entity = self.business_entity
        bank = business_entity.bank

        bank_form = ''
        if bank:
            bank_form = BankDetailForm(instance=bank)

        context['bank_form'] = bank_form
        context['business_entity'] = business_entity
        return context


class BankCreateView(BusinessEntityMixin, CreateView):
    model = Bank
    form_class = BankCreateForm
    template_name = 'banks/create.html'

    def form_valid(self, form):
        bank = form.save()
        business_entity = self.business_entity
        business_entity.bank = bank
        business_entity.save()

        context = {
            'bank_form': BankDetailForm(instance=bank),
            'business_entity': business_entity,
        }

        return render(self.request, 'banks/detail.html', context)

    def form_invalid(self, form):
        context = {
            'bank_form': form,
            'business_entity': self.business_entity,
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_form'] = BankCreateForm()
        context['business_entity'] = self.business_entity
        return context


class BankUpdateView(BusinessEntityMixin, UpdateView):
    model = Bank
    form_class = BankUpdateForm
    template_name = 'banks/partials/forms/_update.html'

    def get_object(self, queryset=None):
        return self.business_entity.bank

    def form_valid(self, form):
        bank = form.save()
        business_entity = self.business_entity
        business_entity.bank = bank
        business_entity.save()

        context = {
            'bank_form': BankDetailForm(instance=bank),
            'business_entity': business_entity,
        }
        return render(self.request, 'banks/detail.html', context)

    def form_invalid(self, form):
        context = {
            'bank_form': form,
            'business_entity': self.business_entity,
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_entity'] = self.business_entity
        context['bank_form'] = BankUpdateForm(instance=self.business_entity.bank)
        return context


class BankDeleteView(BusinessEntityMixin, View):
    template_name = 'banks/detail.html'

    def get(self, request, *args, **kwargs):
        business_entity = self.business_entity
        business_entity.bank = None
        business_entity.save()

        context = {
            'bank_form': '',
            'business_entity': business_entity,
        }

        return render(request, self.template_name, context)
