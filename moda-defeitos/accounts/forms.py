from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from core.models import UserProfile


class BuyerRegistrationForm(UserCreationForm):
    name = forms.CharField(label='Nome completo', max_length=150)
    email = forms.EmailField(label='E-mail', max_length=150)
    phone = forms.CharField(label='Telefone', max_length=20, required=False)
    terms = forms.BooleanField(label='Li e aceito os termos de uso e a política de privacidade.')
    role = UserProfile.Role.BUYER
    profile_fields = ['phone']

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone', 'password1', 'password2', 'terms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autocomplete'] = 'name'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['phone'].widget.attrs['autocomplete'] = 'tel'

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        users = get_user_model().objects.filter(Q(email__iexact=email) | Q(username__iexact=email))
        if users.exists():
            raise forms.ValidationError('Já existe uma conta com este e-mail.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        self.instance.username = cleaned_data.get('email', '')
        self.instance.first_name = cleaned_data.get('name', '')
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile_data = {field: self.cleaned_data[field] for field in self.profile_fields}
            UserProfile.objects.create(
                user=user,
                role=self.role,
                terms_accepted_at=timezone.now(),
                **profile_data,
            )
        return user


class SellerRegistrationForm(BuyerRegistrationForm):
    store_name = forms.CharField(label='Nome da loja', max_length=120, required=False)
    document = forms.CharField(label='CPF', max_length=14)
    location = forms.CharField(label='Cidade e estado', max_length=120)
    role = UserProfile.Role.SELLER
    document_length = 11
    profile_fields = ['phone', 'store_name', 'document', 'location']

    class Meta(BuyerRegistrationForm.Meta):
        fields = [
            'name', 'email', 'phone', 'store_name', 'document', 'location',
            'password1', 'password2', 'terms',
        ]

    def clean_document(self):
        document = self.cleaned_data['document']
        for separator in '.-/ ':
            document = document.replace(separator, '')
        if not document.isascii() or not document.isdigit() or len(document) != self.document_length:
            raise forms.ValidationError(f'Informe um documento com {self.document_length} dígitos.')
        return document


class BrandRegistrationForm(SellerRegistrationForm):
    name = forms.CharField(label='Responsável pela marca', max_length=150)
    store_name = forms.CharField(label='Nome da marca', max_length=120)
    document = forms.CharField(label='CNPJ', max_length=18)
    legal_name = forms.CharField(label='Razão social', max_length=150)
    segment = forms.ChoiceField(label='Atividade principal', choices=[
        ('', 'Selecione uma opção'),
        ('moda', 'Moda e vestuário'),
        ('acessorios', 'Acessórios'),
        ('calcados', 'Calçados'),
        ('casa', 'Casa e decoração'),
    ])
    social = forms.CharField(label='Site ou Instagram', max_length=200, required=False)
    role = UserProfile.Role.BRAND
    document_length = 14
    profile_fields = SellerRegistrationForm.profile_fields + ['legal_name', 'segment', 'social']

    class Meta(BuyerRegistrationForm.Meta):
        fields = [
            'store_name', 'document', 'legal_name', 'segment', 'location',
            'name', 'email', 'phone', 'social', 'password1', 'password2', 'terms',
        ]
