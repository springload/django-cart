from django.http import Http404
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .cart import Cart, ItemDoesNotExist
from .models import Item
from .serializers import CartSerializer, ItemSerializer
from .decorators import cart_required


class CartView(APIView):
    """
        View Cart
        * Only able to request user's session-related cart.
    """

    def get(self, request, format=None):
        """
        Return a related-session cart.
        """
        cart = Cart.get(request)
        if cart:
            serialized_cart = CartSerializer(cart.cart)
            serialized_cart.data['pre_tax_total'] = cart.pre_tax_total()
            serialized_cart.data['total'] = cart.total()
            return Response(serialized_cart.data)
        raise Http404


class ItemDetail(APIView):
    """
    Retrieve, update or delete a Item instance.
    """
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    @cart_required
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    @cart_required
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            cart = Cart.get(request)
            if not cart:
                raise Http404
            product = item.product
            try:
                cart.update(product, serializer.validated_data['quantity'], serializer.validated_data['unit_price'])
            except ItemDoesNotExist:
                raise Http404
            # TODO Jordi check if we need the whole cart or just the item
            # item = self.get_object(pk)
            serializer = CartSerializer(cart.cart)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @cart_required
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        cart = Cart.get(request)
        if not cart:
            raise Http404
        product = item.product
        try:
            cart.remove(product)
        except ItemDoesNotExist:
            raise Http404

        serializer = CartSerializer(cart.cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ItemList(APIView):
    """
        Create a new item
    """
    def post(self, request, format=None):
        cart = Cart.get(request)
        if cart is None:
            cart = Cart(request)

        serializer = ItemSerializer(data=request.data)

        if serializer.is_valid():
            try:
                data_content_type = [x for x in request.data['content_type'].split('.')]
                content_type = ContentType.objects.get(app_label=data_content_type[0], model=data_content_type[1])
                product = content_type.get_object_for_this_type(pk=request.data['object_id'])
            except:
                raise Http404

            cart.add(product, unit_price=serializer.validated_data['unit_price'], quantity=serializer.validated_data['quantity'], )
            try:
                item = Item.objects.get(
                    cart=cart.cart,
                    product=product,
                )
            except:
                raise Http404

            serializer = CartSerializer(cart.cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def cart_count(request):
    """
        Simple method to retry the number of items attached to the request-based cart. Set to 0 if no cart attached to the session yet.
    """
    if request.method == 'GET':
        cart = Cart.get(request)
        if cart:
            count = cart.count()
        else:
            count = 0
        return Response({"count": count})
