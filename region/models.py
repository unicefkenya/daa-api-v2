from django.db import models

# Create your models here.
from mylib.mygenerics import MyModel


class Region(MyModel):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ("id",)


class District(MyModel):
    region = models.ForeignKey(Region, related_name="districts", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return "{}->{}".format(self.region.name, self.name)

    class Meta:
        ordering = ("id",)


class Village(MyModel):
    district = models.ForeignKey(District, related_name="villages", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=45)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "{}->{}->{}".format(self.district.region.name, self.district.name, self.name)

    class Meta:
        ordering = ("id",)


class County(MyModel):
    name = models.CharField(unique=True, max_length=45)
    number = models.CharField(null=True, blank=True, max_length=45)
    headquarters = models.CharField(null=True, blank=True, max_length=45)

    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": None,
            "SCHT": None,
            "CO": "id",
            "SCO": "sub_counties__id",
        }

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name


class SubCounty(MyModel):
    county = models.ForeignKey(County, related_name="sub_counties", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=45)
    partner_names = models.TextField( max_length=200,null=True,blank=True)    
    
    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": None,
            "SCHT": None,
            "CO": "county_id",
            "SCO": "id",
        }

    class Meta:
        ordering = ("county", "name")

    def __str__(self):
        return "{} - {}".format(self.county.name, self.name)
