import datetime
import cart.models as models
from decimal import Decimal

CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)

        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    @staticmethod
    def get(request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart_exists = models.Cart.objects.filter(id=cart_id, checked_out=False).count() or False
            except models.Cart.DoesNotExist:
                cart_exists = False
        else:
            cart_exists = False
        if cart_exists:
            return Cart(request)
        else:
            return None

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1):
        assert self.cart is not None
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = Decimal(quantity)
            item.save()

    def remove(self, product):
        assert self.cart is not None
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        assert self.cart is not None
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:  # ItemAlreadyExists
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = Decimal(quantity)
                item.save()

    def pre_tax_total(self):
        assert self.cart is not None
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result

    def total(self):
        assert self.cart is not None
        result = self.pre_tax_total()
        if self.cart.tax_rate > 0:
            result += result * self.cart.tax_rate
        return result

    def clear(self):
        assert self.cart is not None
        for item in self.cart.item_set.all():
            item.delete()
