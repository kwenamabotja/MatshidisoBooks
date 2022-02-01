from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from main.models import Book, OrderItem, Order, RequestLog
from main.utils.my_utils import MyUtil


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


class TestMyUtil(TestCase):

    def setUp(self) -> None:
        """Set up test data."""
        self.log1 = RequestLog.objects.create(
            ip_address="127.0.0.1",
            input="{\"params\":{\"q\":\"je cherche un mot\"}}",
        )
        self.u = MyUtil()

    def test_save_request(self) -> None:
        assert self.log1 is not None

        pk = self.u.save_request(
            input=self.log1.input,
            ip=self.log1.ip_address,
        )
        assert pk == 2

        self.u.save_response(id=pk, output="{}", response_code=200)

    def test_request(self) -> None:
        response = self.client.get("/")
        assert response.status_code == 200