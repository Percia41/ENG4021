from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import BrandRegistrationForm, BuyerRegistrationForm, SellerRegistrationForm


def register(request, role):
    registration_forms = {
        'buyer': (BuyerRegistrationForm, 'Crie sua conta de comprador'),
        'seller': (SellerRegistrationForm, 'Crie sua conta de vendedor'),
        'brand': (BrandRegistrationForm, 'Apresente sua marca ao FioFora'),
    }
    form_class, title = registration_forms[role]
    form = form_class(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
        except IntegrityError:
            form.add_error(None, 'Não foi possível criar a conta. Confira os dados e tente novamente.')
        else:
            messages.success(request, 'Conta criada. Entre com seu e-mail e senha.')
            return redirect('login_page')
    return render(request, 'accounts/register.html', {'form': form, 'title': title})


def login_page(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'core/login/login.html')


def password_reset_page(request):
    return render(request, 'core/login/password_reset.html', {'demo_notice': request.method == 'POST'})


def account_type_page(request):
    return render(request, 'core/login/account_type.html')
