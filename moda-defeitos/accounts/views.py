from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AccountProfileForm, BrandRegistrationForm, BuyerRegistrationForm,
    EmailAuthenticationForm, SellerRegistrationForm,
)


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        expiry = settings.SESSION_COOKIE_AGE if form.cleaned_data['remember'] else 0
        self.request.session.set_expiry(expiry)
        return response

    def get_success_url(self):
        return reverse('home')


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


def password_reset_page(request):
    return render(request, 'core/login/password_reset.html', {'demo_notice': request.method == 'POST'})


def account_type_page(request):
    return render(request, 'core/login/account_type.html')


@login_required
def account_page(request):
    form = AccountProfileForm(request.user)
    if request.method == 'POST':
        form = AccountProfileForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['password']:
                update_session_auth_hash(request, user)
            messages.success(request, 'Seus dados foram atualizados.')
            return redirect('account_page')

    profile = getattr(request.user, 'profile', None)
    display_name = request.user.get_full_name() or request.user.username
    return render(request, 'accounts/account.html', {
        'form': form,
        'profile': profile,
        'initials': display_name[:2].upper(),
    })
