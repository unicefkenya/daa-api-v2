# Generated by Django 3.1.4 on 2022-01-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0048_auto_20211123_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='knows_dob',
            field=models.BooleanField(default=True),
        ),
    ]
