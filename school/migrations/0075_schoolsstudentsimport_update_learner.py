# Generated by Django 3.1.4 on 2023-06-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0074_auto_20230601_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsstudentsimport',
            name='update_learner',
            field=models.BooleanField(default=False),
        ),
    ]
