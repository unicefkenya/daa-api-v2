# Generated by Django 3.1.4 on 2022-02-22 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0050_auto_20220222_1710'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['id', 'gender'], name='students_id_gender_indx'),
        ),
    ]
