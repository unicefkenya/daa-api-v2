# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-20 10:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_studentabsentreason_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentabsentreason',
            unique_together=set([('student', 'date')]),
        ),
    ]
