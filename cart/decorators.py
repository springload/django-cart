from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status

from .cart import Cart


def cart_required(fn):
    """
    Decorator to check if the user owns the cart (session-based) of the involved Item
    """

    def _check(view, request, pk, *args, **kwargs):

        cart = Cart.get(request)
        if not cart:
            raise Http404

        try:
            item = view.get_object(pk)
        except ObjectDoesNotExist:
            content = {'error': 'cart_item does not exist'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Check item belongs to cart
        if item.cart.id == cart.cart.id:
            # user owns the cart, call the function with all params
            return fn(view, request, pk, *args, **kwargs)
        else:
            content = {'error': 'forbidden'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    return _check
