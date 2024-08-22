# Generated by Django 3.1.4 on 2023-01-17 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0071_student_cash_transfer_beneficiary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('OOSC', 'Dropped Out'), ('NE', 'Never Been to School'), ('PE', 'Previously Enrolled')], default='NE', max_length=5),
        ),
    ]