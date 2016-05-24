from rest_framework import serializers

from .models import Cart, Item


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = ('creation_date', 'currency_code', 'tax_rate', 'exchange_rate')
