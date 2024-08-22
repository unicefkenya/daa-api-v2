# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-19 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20190719_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.CharField(choices=[('A', 'Admin'), ('SA', 'School Admin'), ('T', 'Teacher')], default='A', max_length=45),
        ),
    ]
