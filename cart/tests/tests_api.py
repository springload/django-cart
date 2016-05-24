from decimal import Decimal

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from cart.cart import Cart, CART_ID
from .utils import _create_user_in_database, _create_item_in_database


class CartApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.request = APIRequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

    def test_api_cart_items(self):
        cart = Cart(self.request)
        session = self.client.session
        session[CART_ID] = cart.cart.id
        session.save()
        user = _create_user_in_database()
        _create_item_in_database(cart.cart, user, quantity=1.5, unit_price=Decimal("100"))
        response = self.client.get(reverse('cart_cart'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency_code'], 'USD')
        self.assertEqual(response.data['exchange_rate'], '1.000000')
        self.assertEqual(response.data['tax_rate'], '0.00')
        items = response.data['item_set']
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['serialized_product']['model'], 'auth.user')
        self.assertEqual(items[0]['serialized_product']['fields']['username'], user.username)
        self.assertEqual(items[0]['serialized_product']['fields']['email'], user.email)

    def test_api_items(self):
        cart = Cart(self.request)
        session = self.client.session
        session[CART_ID] = cart.cart.id
        session.save()
        user = _create_user_in_database()
        item = _create_item_in_database(cart.cart, user, quantity=1.5, unit_price=Decimal("100"))
        response = self.client.get(reverse('cart_item', kwargs={'pk': item.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unit_price'], '100.00')
        self.assertEqual(response.data['total_price'], 150)
        self.assertEqual(response.data['serialized_product']['model'], 'auth.user')
        self.assertEqual(response.data['serialized_product']['fields']['username'], user.username)
        self.assertEqual(response.data['serialized_product']['fields']['email'], user.email)

    def test_api_invalid_items(self):
        cart = Cart(self.request)
        session = self.client.session
        session[CART_ID] = cart.cart.id
        session.save()
        response = self.client.get(reverse('cart_item', kwargs={'pk': '456789'}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_cart_cart(self):
        cart = Cart(self.request)
        session = self.client.session
        session[CART_ID] = cart.cart.id
        session.save()
        response = self.client.get(reverse('cart_cart'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency_code'], 'USD')
        self.assertEqual(response.data['exchange_rate'], '1.000000')
        self.assertEqual(response.data['tax_rate'], '0.00')

    def test_api_cart_count(self):
        response = self.client.get(reverse('cart_count'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 0})
