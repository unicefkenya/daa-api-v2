# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-20 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20190720_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='is_school_admin',
            field=models.BooleanField(default=False),
        ),
    ]
