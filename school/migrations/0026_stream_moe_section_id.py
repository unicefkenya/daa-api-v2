# Generated by Django 3.1.4 on 2021-07-21 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_student_moe_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='moe_section_id',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
