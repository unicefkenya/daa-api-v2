# Generated by Django 3.1.4 on 2023-01-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0070_auto_20221015_0406'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cash_transfer_beneficiary',
            field=models.BooleanField(default=False),
        ),
    ]
