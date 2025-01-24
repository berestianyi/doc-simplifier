from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from users.forms import CustomLoginForm


class UserLoginView(View):
    def get(self, request):
        form = CustomLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_page')

            form.add_error(None, 'Невірний email або пароль')

        return render(request, 'users/login.html', {'form': form})
