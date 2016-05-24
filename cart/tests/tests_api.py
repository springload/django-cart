from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


class CartApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.request = APIRequestFactory()

    def test_api_cart_count(self):
        response = self.client.get(reverse('cart_count'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 0})
