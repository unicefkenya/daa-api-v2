# Generated by Django 3.1.4 on 2023-09-20 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0077_auto_20230609_1444'),
        ('attendance', '0004_auto_20210803_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='school.student'),
        ),
    ]
