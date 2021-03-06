# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-18 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import oscar.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0007_slugfield_noop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='price_currency',
            field=models.CharField(default=oscar.core.utils.get_default_currency, max_length=12, verbose_name='货币'),
        ),
        migrations.AlterField(
            model_name='line',
            name='price_excl_tax',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='不含税价格'),
        ),
        migrations.AlterField(
            model_name='line',
            name='price_incl_tax',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='含税价格'),
        ),
    ]
