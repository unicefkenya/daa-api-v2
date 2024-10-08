# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-20 10:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=45, unique=True)),
                ('emis_code', models.CharField(max_length=45, unique=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('school_ministry', models.CharField(blank=True, max_length=100, null=True)),
                ('founder_name', models.CharField(blank=True, max_length=70, null=True)),
                ('year_of_foundation', models.DateField(blank=True, null=True)),
                ('ownership', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(choices=[('R', 'Rural'), ('U', 'Urban')], default='R', max_length=2)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('start_of_calendar', models.DateField(blank=True, null=True)),
                ('end_of_calendar', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('lowest_grade', models.CharField(choices=[('P1', 'PI'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4'), ('P5', 'P5'), ('P6', 'P6'), ('P7', 'P7'), ('P8', 'P8')], default='P1', max_length=4)),
                ('highest_grade', models.CharField(choices=[('P1', 'PI'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4'), ('P5', 'P5'), ('P6', 'P6'), ('P7', 'P7'), ('P8', 'P8')], default='P8', max_length=4)),
                ('schooling', models.CharField(choices=[('B', 'Boarding Only'), ('D', 'Day Only'), ('BD', 'Boarding and Day')], default='D', max_length=4)),
                ('village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='region.Village')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=45, unique=True)),
                ('last_attendance', models.DateField(blank=True, null=True)),
                ('base_class', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], default='1', max_length=3)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streams', to='school.School')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateField(auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('emis_code', models.BigIntegerField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('admission_no', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='ML', max_length=2)),
                ('previous_class', models.IntegerField(blank=True, default=0, null=True)),
                ('mode_of_transport', models.CharField(choices=[('PERSONAL', 'Personal Vehicle'), ('BUS', 'School Bus'), ('FOOT', 'By Foot'), ('NS', 'Not Set')], default='NS', max_length=20)),
                ('time_to_school', models.CharField(choices=[('1HR', 'One Hour'), ('-0.5HR', 'Less than 1/2 Hour'), ('+1HR', 'More than one hour.'), ('NS', 'Not Set')], default='NS', max_length=50)),
                ('stay_with', models.CharField(choices=[('P', 'Parents'), ('G', 'Gurdians'), ('A', 'Alone'), ('NS', 'Not Set')], default='NS', max_length=20)),
                ('household', models.IntegerField(default=0, null=True)),
                ('meals_per_day', models.IntegerField(blank=True, default=0, null=True)),
                ('not_in_school_before', models.BooleanField(default=False)),
                ('emis_code_histories', models.CharField(blank=True, max_length=200, null=True)),
                ('total_attendance', models.IntegerField(blank=True, default=0, null=True)),
                ('total_absents', models.IntegerField(blank=True, default=0, null=True)),
                ('last_attendance', models.DateField(blank=True, null=True)),
                ('guardian_name', models.CharField(blank=True, max_length=50, null=True)),
                ('guardian_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('graduated', models.BooleanField(default=False)),
                ('dropout_reason', models.CharField(blank=True, max_length=200, null=True)),
                ('offline_id', models.CharField(blank=True, max_length=20, null=True)),
                ('stream', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.Stream')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date_started_teaching', models.DateField(blank=True, null=True)),
                ('joined_current_school', models.DateField(blank=True, null=True)),
                ('non_delete', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=20)),
                ('qualifications', models.CharField(blank=True, choices=[('UNI', 'UNIVERSITY'), ('COL', 'COLLEGE')], default='COL', max_length=3, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='school.School')),
                ('streams', models.ManyToManyField(blank=True, null=True, related_name='teachers', to='school.Stream')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
