import datetime
from decimal import Decimal
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from cart.models import Cart
from cart.cart import Cart as rCart
from .utils import _create_cart_in_database, _create_user_in_database, _create_item_in_database


class CartAndItemModelsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

    def test_cart_creation(self):
        creation_date = datetime.datetime.now()
        cart = _create_cart_in_database(creation_date)
        id = cart.id

        cart_from_database = Cart.objects.get(pk=id)
        self.assertEquals(cart, cart_from_database)

    def test_item_creation_and_association_with_cart(self):
        """
            This test is a little bit tricky since the Item tracks
            any model via django's content type framework. This was
            made in order to enable you to associate an item in the
            cart with your product model.

            As I wont make a product model here, I will assume my test
            store sells django users (django.contrib.auth.models.User)
            (lol) so I can test that this is working.

            So if you are reading this test to understand the API,
            you just need to change the user for your product model
            in your code and you're good to go.
        """
        user = _create_user_in_database()

        cart = _create_cart_in_database()
        item = _create_item_in_database(cart, user, quantity=1.5, unit_price=Decimal("100"))

        # get the first item in the cart
        item_in_cart = cart.item_set.all()[0]
        self.assertEquals(item_in_cart, item,
                "First item in cart should be equal the item we created")
        self.assertEquals(item_in_cart.product, user,
                "Product associated with the first item in cart should equal the user we're selling")
        self.assertEquals(item_in_cart.unit_price, Decimal("100"),
                "Unit price of the first item stored in the cart should equal 100")
        self.assertEquals(item_in_cart.quantity, 1.50,
                "The first item in cart should have 1.50 in it's quantity")

    def test_total_item_price(self):
        """
        Since the unit price is a Decimal field, prefer to associate
        unit prices instantiating the Decimal class in
        decimal.Decimal.
        """
        user = _create_user_in_database()
        cart = _create_cart_in_database()

        # not safe to do as the field is Decimal type. It works for integers but
        # doesn't work for float
        item_with_unit_price_as_integer = _create_item_in_database(cart, product=user, quantity=1.5, unit_price=200)

        self.assertEquals(item_with_unit_price_as_integer.total_price, 300)

        # this is the right way to associate unit prices
        item_with_unit_price_as_decimal = _create_item_in_database(cart,
                product=user, quantity=4.5, unit_price=300)
        self.assertEquals(item_with_unit_price_as_decimal.total_price, 1350)

    def test_update_cart(self):
        user = _create_user_in_database()
        cart = rCart(self.request)
        cart.new(self.request)
        cart.add(product=user, quantity=3, unit_price=100)
        cart.update(product=user, quantity=2.5, unit_price=55555)
        self.assertEquals(cart.total(), 138888)

    def test_item_unicode(self):
        user = _create_user_in_database()
        cart = _create_cart_in_database()

        item = _create_item_in_database(cart, product=user, quantity=Decimal(3), unit_price=Decimal(100))

        self.assertEquals(item.__unicode__(), "3 units of User")
