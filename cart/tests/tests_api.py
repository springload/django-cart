from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from cart.cart import Cart, CART_ID


class CartApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.request = APIRequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

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
