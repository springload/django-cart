from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class Cart(models.Model):
    app_label = 'cart'
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class Item(models.Model):
    app_label = 'cart'

    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price

    total_price = property(total_price)

    def cart_creation_date(self):
        return self.cart.creation_date

    def product_name(self):
        return ""

    def product_description(self):
        return ""

    def course_xrm_id(self):
        return ""

    def get_item_name(self):
        return str(self)

    def booking_id(self):
        return self.cart.booking.id

    def booking_payment_method(self):
        return self.cart.booking.payment_method

    def payment_transaction_id(self):
        if not hasattr(self, "payment"):
            self.payment = self.cart.payments.latest()
        return str(self.payment.transaction_id)

    def payment_transaction_total(self):
        if not hasattr(self, "payment"):
            self.payment = self.cart.payments.latest()
        return self.payment.total

    def get_booker(self):
        return {
            "first_name": self.cart.booking.first_name,
            "last_name": self.cart.booking.last_name,
            "address1": self.cart.booking.address1,
            "address2": self.cart.booking.address2,
            "address3": self.cart.booking.address3,
            "suburb": self.cart.booking.suburb,
            "organisation_name": self.cart.booking.organisation_name
        }

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)

