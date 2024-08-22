from django.db import models

# Create your models here.
from mylib.mygenerics import MyModel
from school.models import School

from django.conf import settings

MyUser = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')



class SupportQuestion(MyModel):
    title=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True,max_length=2000)



class SupportRequest(MyModel):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,blank=True)
    email=models.EmailField()
    name=models.CharField(max_length=45)
    subject=models.CharField(max_length=900)
    body=models.TextField(max_length=3000)
    phone=models.CharField(max_length=20)

