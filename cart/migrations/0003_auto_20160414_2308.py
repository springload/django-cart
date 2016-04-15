# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20160414_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='currency_code',
            field=models.CharField(default='USD', verbose_name='currency', max_length=20),
        ),
        migrations.AddField(
            model_name='cart',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=6, default=1, verbose_name='Exchange Rate', max_digits=10),
        ),
        migrations.AddField(
            model_name='cart',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
