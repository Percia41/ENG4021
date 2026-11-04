from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from accounts.decorators import buyer_required
from orders.models import OrderItem

from .forms import ReviewForm
from .models import Review
from .services import review_block_reason


@require_POST
@buyer_required
def review_save(request, item_id):
    """Cria a avaliação do item ou edita a que o comprador já fez."""
    # Filtrar pelo dono do pedido faz outro usuário receber 404.
    item = get_object_or_404(OrderItem.objects.select_related('order'), pk=item_id, order__user=request.user)
    back = redirect('order_detail', order_id=item.order_id)

    reason = review_block_reason(item)
    if reason:
        messages.error(request, reason)
        return back

    review = Review.objects.filter(order_item=item).first()
    form = ReviewForm(request.POST, instance=review)
    if not form.is_valid():
        messages.error(request, 'Não foi possível salvar a avaliação. Escolha uma nota de 1 a 5.')
        return back

    new_review = form.save(commit=False)
    new_review.order_item = item
    new_review.user = request.user
    new_review.save()
    messages.success(request, 'Avaliação atualizada.' if review else 'Avaliação enviada. Obrigado!')
    return back
