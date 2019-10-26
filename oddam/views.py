from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
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

    def post(self, request):
        quantity = request.POST['bags']
        categories = request.POST.getlist('categories')
        print(categories)
        institution_id = request.POST['organization']
        address = request.POST['address']
        phone_number = request.POST['phone']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        pick_up_date = request.POST['date']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        user_id = request.POST['user_id']

        user = User.objects.get(pk=user_id)
        institution = Institution.objects.get(pk=institution_id)
        donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number,
                                           city=city, zip_code=zip_code, pick_up_date=pick_up_date,
                                           pick_up_time=pick_up_time, pick_up_comment=pick_up_comment,
                                           institution=institution, user=user)
        for category in categories:
            c = Category.objects.get(name=category)
            donation.categories.add(c)

        return redirect('confirmation')


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


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserDetailView(PermissionRequiredMixin, View):
    permission_required = 'oddam.view_donation'

    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user).filter(is_taken=False)
        taken_donations = Donation.objects.filter(user=user).filter(is_taken=True)

        return render(request, 'user-detail.html', {
            'donations': donations,
            'taken_donations': taken_donations
        })

    def post(self, request):
        donation_id = request.POST['donation_id']
        donation = Donation.objects.get(pk=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect('user_detail')


class UserEditView(View):
    def get(self, request):
        return render(request, 'user-edit.html')

    def post(self, request):
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = request.POST['email']

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = email
        user.save()
        return redirect('user_detail')


class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'password-change.html')

    def post(self, request):
        password = request.POST['password']
        re_password = request.POST['password2']
        user = request.user
        if password == re_password:
            user.set_password(password)
            user.save()
            messages.success(request, 'Zmiana hasła powiodała się!')
            return redirect('login')
        else:
            messages.warning(request, 'Wprowadzone hasła nie są takie same!')
        return render(request, 'password-change.html')


class SendEmailView(View):
    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        message = request.POST['message']
        admins = []
        for user in User.objects.all().filter(is_staff=True):
            admins.append(user.email)

        send_mail(
            'Wiadomość od {} {}'.format(name, surname),
            message,
            'django.send.mail.test.mm@gmail.com',
            admins
        )
        return redirect('landing_page')



