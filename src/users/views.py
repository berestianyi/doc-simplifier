from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .forms import EmailAuthenticationForm, ProfileForm, ProfileDetailForm

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailAuthenticationForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileDetailForm(instance=self.request.user)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user
