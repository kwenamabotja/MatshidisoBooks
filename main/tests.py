from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from main.models import Book, OrderItem, Order


class OrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name="Toto",
            last_name="Tata",
        )
        self.book1 = Book.objects.create(
            title="The swan",
            price=450.00
        )
        self.order = Order.objects.create(
            user=self.user
        )
        self.item1 = OrderItem.objects.create(
            item=self.book1,
            quantity=2,
            order=self.order
        )

    def test_book(self):
        self.assertEqual(450.00, self.book1.price)
        self.assertEqual("The swan", self.book1.title)

    def test_order_a_book(self):
        """"""
        self.assertEqual(1035.00, self.order.total)
        self.assertEqual(1, len(self.order.get_items))
