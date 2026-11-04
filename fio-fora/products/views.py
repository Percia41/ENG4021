from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import seller_required
from favorites.models import mark_favorites

from .forms import DiscountSimulationForm, ProductForm
from .models import FAIXAS_SEVERIDADE, Product


def home(request):
    """Vitrine: peças ativas, com filtro opcional por faixa de severidade (?faixa=leve)."""
    band = request.GET.get('faixa', '')
    if band not in dict(FAIXAS_SEVERIDADE):
        band = ''  # faixa desconhecida: mostra todas as peças
    products = Product.objects.filter(is_active=True).select_related('defeito')
    if band:
        products = products.with_severity_band(band)
    return render(request, 'products/home.html', {
        'products': mark_favorites(products, request.user),
        'bands': FAIXAS_SEVERIDADE,
        'active_band': band,
    })


def product_detail(request, product_id):
    products = (Product.objects.filter(is_active=True)
                .select_related('defeito', 'category', 'seller__profile').prefetch_related('images'))
    product = get_object_or_404(mark_favorites(products, request.user), id=product_id)
    return render(request, 'products/detail.html', {'product': product})


def discount_simulator(request):
    form = DiscountSimulationForm(request.POST if request.method == 'POST' else None)
    result = form.preview() if request.method == 'POST' and form.is_valid() else None
    return render(request, 'products/discount_simulator.html', {'form': form, 'result': result})


@seller_required
def my_products(request):
    products = (Product.objects.filter(seller=request.user)
                .select_related('defeito').prefetch_related('images').order_by('-created_at', '-pk'))
    page = Paginator(products, 12).get_page(request.GET.get('page'))
    return render(request, 'products/my_products.html', {'page_obj': page})


@seller_required
def product_create(request):
    return product_form(request, Product(seller=request.user), 'Cadastrar peça', 'Peça cadastrada com sucesso.')


@seller_required
def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id, seller=request.user)
    return product_form(request, product, 'Editar peça', 'Peça atualizada com sucesso.')


@seller_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'“{product.name}” foi removida.')
        return redirect('my_products')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


def product_form(request, product, title, success_message):
    """Cadastro e edição usam o mesmo formulário e o mesmo template."""
    form = ProductForm(request.POST if request.method == 'POST' else None,
                       request.FILES if request.method == 'POST' else None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, success_message)
        return redirect('my_products')
    return render(request, 'products/product_form.html', {'form': form, 'title': title})
