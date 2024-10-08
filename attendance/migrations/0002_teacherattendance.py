# Generated by Django 3.1.4 on 2021-07-15 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_auto_20210715_1002'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('is_present', models.BooleanField(default=False)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher')),
            ],
            options={
                'ordering': ('id',),
                'abstract': False,
            },
        ),
    ]
