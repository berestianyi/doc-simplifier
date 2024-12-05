from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from business_entities.forms import BusinessEntitiesCreateForm, BusinessEntitiesUpdateForm
from business_entities.models import BusinessEntities


class HomePageView(TemplateView):
    template_name = 'base.html'


class BusinessEntitiesListView(ListView):
    model = BusinessEntities
    template_name = 'business_entity/list.html'
    context_object_name = 'business_entities'
    paginate_by = 10


class BusinessEntityDetailView(FormMixin, DetailView):
    model = BusinessEntities
    template_name = 'business_entity/detail.html'
    context_object_name = 'business_entity'
    pk_url_kwarg = 'entity_id'
    form_class = BusinessEntitiesUpdateForm

    def get_success_url(self):
        return reverse('business_entity_detail', kwargs={'entity_id': self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CreateBusinessEntityView(CreateView):
    model = BusinessEntities
    form_class = BusinessEntitiesCreateForm
    template_name = 'business_entity/create.html'
    success_url = reverse_lazy('business_entities')

    def form_valid(self, form):
        return super().form_valid(form)
