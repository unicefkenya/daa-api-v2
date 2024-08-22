# Generated by Django 3.0.8 on 2021-11-09 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0031_stream_moe_section_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='temp_id',
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('OOSC', 'Out Of School'), ('NWE', 'Newly Enrolled'), ('NVE', 'Never Enrolled'), ('PE', 'Previously Enrolled')], default='NS', max_length=5),
        ),
    ]
