# Generated by Django 3.1.4 on 2022-04-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0059_schoolsstudentsimport_error_rows_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsstudentsimport',
            name='should_import',
            field=models.BooleanField(default=True),
        ),
    ]
