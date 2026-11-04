from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from orders.models import OrderItem

RATING_CHOICES = [
    (1, '1 - Ruim'),
    (2, '2 - Regular'),
    (3, '3 - Bom'),
    (4, '4 - Muito bom'),
    (5, '5 - Excelente'),
]


class Review(models.Model):
    """Avaliação de uma peça comprada. Cada item de pedido tem no máximo uma."""

    # OneToOne garante "uma vez por item" direto no banco, não só na view.
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='review', verbose_name='item do pedido')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name='comprador')
    rating = models.PositiveSmallIntegerField('nota', choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('comentário', max_length=1000, blank=True)
    created_at = models.DateTimeField('criada em', auto_now_add=True)
    updated_at = models.DateTimeField('editada em', auto_now=True)

    class Meta:
        ordering = ['-created_at', '-pk']
        verbose_name = 'avaliação'
        verbose_name_plural = 'avaliações'
        constraints = [models.CheckConstraint(condition=models.Q(rating__range=(1, 5)), name='review_rating_1_to_5')]

    @property
    def stars(self):
        """Nota em estrelas de texto (ex.: ★★★★☆), para mostrar nas listas."""
        return '★' * self.rating + '☆' * (5 - self.rating)

    @property
    def reviewer_name(self):
        """Só o primeiro nome aparece na página pública."""
        parts = self.user.first_name.split()
        return parts[0] if parts else 'Comprador'

    def __str__(self):
        return f'{self.order_item.product_name}: {self.rating}/5'
