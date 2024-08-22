import django_filters
from django_filters.rest_framework import FilterSet

from school.promotion.models import PromoteSchool


class PromoteSchoolFilter(FilterSet):
    school_emis_code=django_filters.NumberFilter(field_name="school__emis_code", label="School emis code")
    #partner=django_filters.NumberFilter(name="",label="Partner  Id",method="filter_partner")
    #partner_admin=django_filters.NumberFilter(name="",label="Partner Admin Id",method="filter_partner_admin")
    #county=django_filters.NumberFilter(name="school__zone__subcounty__county",label="County Id")
    class Meta:
        model=PromoteSchool
        fields=('__all__')