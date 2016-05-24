import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from cart.models import Cart, Item


def _create_cart_in_database(creation_date=datetime.datetime.now(), checked_out=False):
    """
        Helper function so I don't repeat myself
    """
    cart = Cart()
    cart.creation_date = creation_date
    cart.checked_out = False
    cart.save()
    return cart


def _create_item_in_database(cart, product, quantity=1.3, unit_price=Decimal("100")):
    """
        Helper function so I don't repeat myself
    """
    item = Item()
    item.cart = cart
    item.product = product
    item.quantity = quantity
    item.unit_price = unit_price
    item.save()

    return item


def _create_user_in_database():
    """
        Helper function so I don't repeat myself
    """
    user = User(username="user_for_sell", password="sold", email="example@example.com")
    user.save()
    return user
