# Generated by Django 3.1.4 on 2022-04-14 19:44

from django.db import migrations


def update_school_filter_args(apps, schema_editor):
  MyUser = apps.get_model('client', 'MyUser')
  School = apps.get_model('school', 'School')

  for instance in MyUser.objects.all():
    if instance.role=="SCHA" or instance.role=="SCHT":
      if School.objects.filter(emis_code=instance.username).exists():
        instance.filter_args="{}".format(School.objects.get(emis_code=instance.username).id)
        instance.save()





class Migration(migrations.Migration):

    dependencies = [
        ('school', '0063_auto_20220408_0858'),
    ]

    operations = [
      migrations.RunPython(code=update_school_filter_args, )
    ]
