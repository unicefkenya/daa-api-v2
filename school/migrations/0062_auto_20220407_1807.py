# Generated by Django 3.1.4 on 2022-04-07 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0061_auto_20220407_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolsstudentsimport',
            name='step',
            field=models.CharField(choices=[('Q', 'Queued'), ('VH', 'Validating Required Columns...'), ('PI', 'Preparing...'), ('I', 'Processing...'), ('F', 'Failed'), ('D', 'Done')], default='Q', editable=False, max_length=3),
        ),
    ]