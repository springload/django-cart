import json
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.contrib.contenttypes.fields import GenericRelation


class Cart(models.Model):

    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    currency_code = models.CharField(default='USD', verbose_name=_('currency'), max_length=20)
    tax_rate = models.DecimalField(default=0, max_digits=6, decimal_places=4)
    exchange_rate = models.DecimalField(default=1, verbose_name=_('Exchange Rate'), max_digits=10, decimal_places=6)

    def checkout(self):
        self.checked_out = True
        self.save()

    @property
    def pre_tax_total(self):
        result = 0
        for item in self.items.all():
            result += item.total_price
        return result

    @property
    def total(self):
        result = self.pre_tax_total
        if self.tax_rate > 0:
            result += result * self.tax_rate
        return '{0:.2f}'.format(result)

    def clear(self):
        for item in self.items.all():
            item.delete()

    @property
    def count(self):
        return self.items.all().count()

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __str__(self):
        return 'Cart  {0} Created: {1}'.format(self.id, self.creation_date)

    def add_item(self, product, unit_price, quantity=1):
        try:
            item = Item.objects.get(
                cart=self,
                product=product,
            )
        except Item.DoesNotExist:
            item = Item(
                cart=self,
                product=product,
                unit_price=unit_price,
            )
            item.cart = self
            item.product = product
            item.unit_price = unit_price
            item.quantity = Decimal(quantity)
            item.save()

        return item


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), related_name=_('items'))
    quantity = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    # Support for uuids and int Ids
    object_id = models.CharField(max_length=128)

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    @property
    def total_price(self):
        r = self.quantity * self.unit_price
        return int(round(r, 0))

    """
    @cached_property
    def product(self):
        return self.get_product()
    """

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def product_name(self):
        return self.product.__str__()

    @property
    def product_type(self):
        return self.content_type.name

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    def serialized_product(self, format='json'):
        # bit hacky but works
        return json.loads(serializers.serialize(format, [self.product, ]))[0]

    product = property(get_product, set_product)
