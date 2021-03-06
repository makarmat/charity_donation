"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from oddam.views import LandingPage, AddDonation, LoginView, RegisterView, LogoutView, ConfirmationView, UserDetailView, \
    UserEditView, ChangePasswordView, SendEmailView, CheckPasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing_page'),
    path('add_donation/', AddDonation.as_view(), name='add_donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add_donation/form-confirmation.html', ConfirmationView.as_view(), name='confirmation'),
    path('user-detail/', UserDetailView.as_view(), name='user_detail'),
    path('user-edit/', UserEditView.as_view(), name='user_edit'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('check-password/', CheckPasswordView.as_view(), name='check_password'),
    path('send-mail/', SendEmailView.as_view(), name='send_mail'),

]
