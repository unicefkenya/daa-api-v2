# Generated by Django 3.1.4 on 2023-06-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0073_school_is_training_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('OOSC', 'Dropped Out'), ('NE', 'Never Been to School'), ('PE', 'Already Enrolled')], default='NE', max_length=5),
        ),
    ]