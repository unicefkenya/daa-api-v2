# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-30 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_auto_20190730_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='name',
            field=models.CharField(blank=True, default='', max_length=45, null=True),
        ),
    ]
