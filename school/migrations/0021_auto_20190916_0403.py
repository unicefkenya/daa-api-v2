# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-09-16 01:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0020_auto_20190913_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_enrolled',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]