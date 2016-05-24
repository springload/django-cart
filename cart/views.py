from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .cart import Cart
from .serializers import CartSerializer


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
            return Response(serialized_cart.data)
        return Response()


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
