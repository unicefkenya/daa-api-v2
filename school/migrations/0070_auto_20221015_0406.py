# Generated by Django 3.1.4 on 2022-10-15 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0069_auto_20221014_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolsstudentsimport',
            name='import_type',
            field=models.CharField(choices=[('F', 'Import File'), ('NMC', 'Nemis County'), ('NMSC', 'Nemis Sub County'), ('NMSCH', 'Nemis School'), ('JS', 'Json Data')], default='F', max_length=5),
        ),
    ]