# Generated by Django 3.1.4 on 2021-08-03 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_teacherattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherattendance',
            name='id',
            field=models.CharField(max_length=70, primary_key=True, serialize=False),
        ),
    ]