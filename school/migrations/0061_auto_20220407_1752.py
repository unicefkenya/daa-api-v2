# Generated by Django 3.1.4 on 2022-04-07 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0060_schoolsstudentsimport_should_import'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schoolsstudentsimport',
            options={'ordering': ('-id',)},
        ),
    ]
