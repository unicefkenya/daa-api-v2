from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models

# Create your models here.
from mylib.mygenerics import MyModel
from school.models import Stream, GraduatesStream, School, Student


# class Promotions(MyModel):
#     prev_class=models.ForeignKey(Stream, related_name="previous_class")
#     student = models.ForeignKey(Student,on_delete=models.CASCADE)
#     next_class = models.ForeignKey(Stream, related_name="next_class")
#
#     def __str__(self):
#         return "%s to %s" % (self.prev_class,self.next_class)


class PromoteSchoolManager(models.Manager):
    def get_queryset(self):
        return super(PromoteSchoolManager, self).get_queryset()



class PromoteSchool(MyModel):
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    completed=models.BooleanField(default=False)
    year = models.PositiveSmallIntegerField(max_length=4)
    graduates_class=models.ForeignKey(GraduatesStream,null=True,blank=True,on_delete=models.SET_NULL)
    objects=PromoteSchoolManager()

    def __str__(self):
        return "%s (%s) "%(self.school.name,self.year)

    def complete(self):
        #Get all the promotions and order them from class 8
        proms=list(PromoteStream.objects.filter(promote_school_id=self.id).order_by("-prev_class__base_class"))


        #Graduate class 8 and make the inactive
        Student.objects.filter(stream__school_id=self.school_id,stream__base_class='8').update(active=False,stream=None,graduated=True,graduates_class_id=self.graduates_class_id)

        # For the rest starting with class 7 & change the prev class id to next_class id
        for p in proms:
            d=Student.objects.filter(stream_id=p.prev_class_id).update(stream_id=p.next_class_id)
            p.completed = True
            p.save()
        self.completed=True
        self.save()

    def undo(self):
        proms = list(PromoteStream.objects.filter(promote_school_id=self.id).order_by("prev_class__base_class"))
        for p in proms:
            d=Student.objects.filter(stream_id=p.next_class_id).update(stream_id=p.prev_class_id)
            p.completed=False
            p.save()
            # print (p.next_class.class_name, d)
        ##revert Class 8
        cl8_id=proms[-1].next_class.id
        # print ("Class 8 promote stream ",cl8_id)
        d=Student.objects.filter(graduates_class_id=self.graduates_class_id).update(active=True,
                                                                                              stream_id=cl8_id,
                                                                                              graduated=False,
                                                                                           )
        # print ("reverted ",d)
        self.completed = False
        self.save()
        GraduatesStream.objects.filter(id=self.graduates_class_id).delete()
        self.delete()


    def save(self,  *args, **kwargs):
        if self.id is None:
            g=GraduatesStream(school=self.school,year=self.year)
            g.save()
            self.graduates_class_id=g.id
        else:
            GraduatesStream.objects.filter(id=self.graduates_class_id).update(school=self.school,year=self.year)
        super(PromoteSchool, self).save(*args, **kwargs)


class PromoteStream(MyModel):
    prev_class=models.ForeignKey(Stream,related_name="prev_class",on_delete=models.PROTECT)
    next_class=models.ForeignKey(Stream,related_name="next_class",on_delete=models.PROTECT)
    completed=models.BooleanField(default=False)
    promote_school=models.ForeignKey(PromoteSchool,related_name="stream_promotions",on_delete=models.CASCADE)


    def __str__(self):
        return "%s to %s" %(self.prev_class.class_name,self.next_class.class_name)
