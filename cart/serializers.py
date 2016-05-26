
from rest_framework import serializers

from .models import Cart, Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    content_type = serializers.StringRelatedField(many=False, read_only=True)
    cart = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    quantity = serializers.DecimalField(decimal_places=2, max_digits=18, required=False)
    unit_price = serializers.DecimalField(decimal_places=2, max_digits=18, required=False)

    class Meta:
        model = Item
        fields = ('pk', 'cart', 'object_id', 'quantity', 'unit_price', 'total_price', 'content_type', 'serialized_product')
        read_only_fields = ('pk', 'cart', 'object_id', 'total_price', 'content_type', 'serialized_product')


class CartSerializer(serializers.HyperlinkedModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('pk', 'creation_date', 'currency_code', 'tax_rate', 'exchange_rate', 'item_set')
