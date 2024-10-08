# Generated by Django 3.1.4 on 2022-10-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0067_auto_20221014_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsstudentsimport',
            name='raw_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolsstudentsimport',
            name='import_type',
            field=models.CharField(choices=[('F', 'Import File'), ('NC', 'Nemis County'), ('NMSC', 'Nemis Sub County'), ('NMSCH', 'Nemis School'), ('JS', 'Json Data')], default='F', max_length=5),
        ),
    ]
