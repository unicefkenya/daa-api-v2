# Generated by Django 3.1.4 on 2021-07-15 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_auto_20190916_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
