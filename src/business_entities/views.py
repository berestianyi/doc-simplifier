from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from business_entities.forms import BusinessEntitiesForm
from business_entities.models import BusinessEntities


class HomePageView(TemplateView):
    template_name = 'base.html'


class BusinessEntitiesListView(ListView):
    model = BusinessEntities
    template_name = 'business_entity/list.html'
    context_object_name = 'business_entities'
    paginate_by = 10


class BusinessEntityDetailView(DetailView):
    model = BusinessEntities
    template_name = 'business_entity/detail.html'
    context_object_name = 'business_entity'
    pk_url_kwarg = 'entity_id'


class CreateBusinessEntityView(CreateView):
    model = BusinessEntities
    form_class = BusinessEntitiesForm
    template_name = 'business_entity/create.html'
    success_url = reverse_lazy('business_entities')

    def form_valid(self, form):
        data = form.cleaned_data
        edrpou = data.get('edrpou', '').strip()

        if len(edrpou) == 8:
            form.instance.business_entity = BusinessEntities.BusinessEntitiesEnum.FOP
        elif len(edrpou) == 10:
            form.instance.business_entity = BusinessEntities.BusinessEntitiesEnum.TOV
        else:
            form.add_error('edrpou', 'Неправильний код ЕДРПОУ')
            return self.form_invalid(form)

        return super().form_valid(form)
