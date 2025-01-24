from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('users:user_login'),
            # reverse('admin:login'),  # админка (если надо)
            # reverse('admin:index')
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(url) for url in self.exempt_urls):
                return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response
