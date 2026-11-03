from decimal import Decimal
from io import StringIO

from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase

from cart.models import CartItem
from favorites.models import Favorite
from products.models import Defeito, Product

from .models import Order


class OrderHistoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("popular_banco", stdout=StringIO())

    def test_financial_history_and_database_integrity(self):
        order = Order.objects.get(reference="FF-DEMO-PEDIDO-001")
        self.assertEqual(order.total, Decimal("104.00"))
        product = order.items.get().product
        product.name = "Novo nome"
        product.price = Decimal("99.00")
        product.save()
        self.assertEqual(order.items.get().product_name, "Vestido floral")
        self.assertEqual(order.total, Decimal("104.00"))
        with self.assertRaises(IntegrityError), transaction.atomic():
            Favorite.objects.create(user_id=Favorite.objects.first().user_id, product_id=Favorite.objects.first().product_id)
        with self.assertRaises(IntegrityError), transaction.atomic():
            CartItem.objects.filter(pk=CartItem.objects.first().pk).update(quantity=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Defeito.objects.filter(product=product).update(tipo=4)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.filter(pk=product.pk).update(price=Decimal("0.00"))
