"""Regras do carrinho, usadas também pelo checkout (orders)."""
from decimal import Decimal

from .models import Cart

MAX_QUANTITY = 99
CENTS = Decimal('0.01')


def parse_quantity(raw):
    """Converte o texto enviado em inteiro de 1 a MAX_QUANTITY; devolve None se inválido."""
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        return None
    return value if 1 <= value <= MAX_QUANTITY else None


def unavailable_reason(product, quantity):
    """Motivo pelo qual `quantity` unidades da peça não podem ser compradas (ou None)."""
    if not product.is_active:
        return 'Esta peça não está mais à venda.'
    if product.stock < 1:
        return 'Peça esgotada.'
    if quantity > product.stock:
        unit = 'unidade' if product.stock == 1 else 'unidades'
        return f'Só há {product.stock} {unit} em estoque.'
    return None


def build_cart_summary(user):
    """Monta as linhas do carrinho e o total, calculados a partir do banco."""
    cart = Cart.objects.filter(user=user).first()
    lines, total, pieces = [], Decimal('0.00'), 0
    if cart is not None:
        items = cart.items.select_related('product').order_by('pk')
        for item in items:
            product = item.product
            problem = unavailable_reason(product, item.quantity)
            subtotal = (product.price * item.quantity).quantize(CENTS)
            lines.append({
                'item': item,
                'product': product,
                'subtotal': subtotal,
                'problem': problem,
                'max_quantity': max(1, min(product.stock, MAX_QUANTITY)),
            })
            # Itens indisponíveis ficam visíveis (para o comprador ajustar ou remover),
            # mas não entram no total.
            if problem is None:
                total += subtotal
                pieces += item.quantity
    return {
        'lines': lines,
        'total': total,
        'pieces': pieces,
        'has_unavailable': any(line['problem'] for line in lines),
    }
