# Generated by Django 3.1.4 on 2021-11-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0041_student_guardian_sub_county'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='guardian_email',
            field=models.EmailField(blank=True, max_length=45, null=True),
        ),
    ]
