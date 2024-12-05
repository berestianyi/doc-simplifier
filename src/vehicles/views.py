from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from .forms import VehiclesCreateForm, VehiclesUpdateForm
from vehicles.models import Vehicles


class VehiclesListView(ListView):
    model = Vehicles
    template_name = 'vehicles/list.html'
    context_object_name = 'vehicles'
    paginate_by = 10


class VehicleDetailView(FormMixin, DetailView):
    model = Vehicles
    template_name = 'vehicles/detail.html'
    context_object_name = 'vehicle'
    pk_url_kwarg = 'vehicle_id'
    form_class = VehiclesUpdateForm

    def get_success_url(self):
        return reverse('vehicle_detail', kwargs={'vehicle_id': self.object.id})

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


class CreateVehicleView(CreateView):
    model = Vehicles
    form_class = VehiclesCreateForm
    template_name = 'vehicles/create.html'
    success_url = reverse_lazy('vehicles')

    def form_valid(self, form):
        return super().form_valid(form)

