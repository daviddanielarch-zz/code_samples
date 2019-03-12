from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views import View

from django.contrib.auth import login, authenticate
from custom_auth.forms import CreateUserForm
from django.shortcuts import render, redirect


class CustomLoginView(LoginView):
    template_name = 'login.html'


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = CreateUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = email.split('@')[0]
            raw_password = form.cleaned_data.get('password1')
            User.objects.create(email=email, username=username, password=raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, {'form': form})

