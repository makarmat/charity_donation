from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = 'index.html'


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
