from django.http import Http404

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .cart import Cart
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
    Retrieve, update or delete a snippet instance.
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
