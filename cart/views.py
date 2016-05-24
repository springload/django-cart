from rest_framework.response import Response
from rest_framework.decorators import api_view
from .cart import Cart


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
