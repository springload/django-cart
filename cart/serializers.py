
from rest_framework import serializers

from .models import Cart, Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    content_type = serializers.StringRelatedField(many=False)
    cart = serializers.StringRelatedField(many=False)

    class Meta:
        model = Item
        fields = ('pk', 'cart', 'quantity', 'unit_price', 'total_price', 'content_type', 'serialized_product')
        read_only_fields = ('pk', 'cart', 'total_price', 'content_type', 'serialized_product')


class CartSerializer(serializers.HyperlinkedModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('pk', 'creation_date', 'currency_code', 'tax_rate', 'exchange_rate', 'item_set')
