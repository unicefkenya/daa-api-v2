from django.contrib import admin

# Register your models here.
from django.apps import apps

app_models = apps.get_app_config('attendance').get_models()
from django.contrib.admin.sites import AlreadyRegistered

for model in app_models:
    try:
        attrs={"list_display" : [f.name for f in model._meta.get_fields() if not f.many_to_many and not f.one_to_many]}
        name="Admin_"+model.__name__
        theclass=type(str(name),(admin.ModelAdmin,),attrs)
        admin.site.register(model,theclass)
    except AlreadyRegistered:
        pass