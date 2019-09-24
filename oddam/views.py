from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from oddam.models import Donation, Institution


class LandingPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        donations = Donation.objects.all()
        bags_quantity = 0
        for donation in donations:
            bags_quantity += donation.quantity

        donated_institutions = [i.institution.id for i in donations.exclude(institution=None)]
        institution_quantity = len(list(set(donated_institutions)))

        context = super(LandingPage, self).get_context_data(**kwargs)
        context['bags_quantity'] = bags_quantity
        context['institution_quantity'] = institution_quantity
        return context


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
