from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from oddam.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        donations = Donation.objects.all()
        bags_quantity = 0
        for donation in donations:
            bags_quantity += donation.quantity

        institution_quantity = Donation.objects.all().values('institution').annotate(total=Count('institution')).order_by('total').count()

        fundations_list = Institution.objects.filter(type=1)
        ngos = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)

        paginator = Paginator(fundations_list, 5)
        page = request.GET.get('page')
        fundations = paginator.get_page(page)
        args = {
            'bags_quantity': bags_quantity,
            'institution_quantity': institution_quantity,
            'fundations': fundations,
            'ngos': ngos,
            'local_collections': local_collections,
        }

        return render(request, 'index.html', args)


class AddDonation(PermissionRequiredMixin, View):
    permission_required = 'oddam.add_donation'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {
            'categories': categories,
            'institutions': institutions
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not User.objects.filter(username=username).exists():
            messages.warning(request, 'Użytkownik o loginie "{}" nie istnieje!'.format(username))
            return redirect('register')
        elif user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            messages.warning(request, 'Hasło nieprawidłowe!')
            return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        users_list = [user.email for user in User.objects.all()]
        if '@' not in email:
            messages.warning(request, 'Wprowadzono niepoprawny e-mail!')
            return render(request, 'register.html')
        elif email in users_list:
            messages.warning(request, 'Użytkownik z tym adresem e-mail już istnieje!')
            return render(request, 'register.html')
        elif password != password2:
            messages.warning(request, 'Powtórzone hasło nie jest takie samo!')
            return render(request, 'register.html')
        User.objects.create_user(username=email, first_name=name, last_name=surname, email=email, password=password)
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')

