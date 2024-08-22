import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend

from attendance.models import Attendance
from mylib.my_common import str2bool
from school.models import STUDENT_STATUS
import mylib.my_common as my_common
from django.contrib.auth import get_user_model
from django.db.models import Count
User=get_user_model()

class AttendanceFilter(FilterSet):
    GENDERS = (
        ("M", "Male"),
        ("F", "Female"),
    )
    base_class = django_filters.CharFilter(field_name="stream__base_class", label="Class")
    date = django_filters.DateFilter(field_name="date__date", label="date")
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte", label="Start Date")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr=("lte"), label="End Date")
    gender = django_filters.ChoiceFilter(field_name="student__gender", label="gender", choices=GENDERS)
    learner_status = django_filters.ChoiceFilter(field_name="student__status", label="Leaner Status", choices=STUDENT_STATUS)
    school = django_filters.NumberFilter(field_name="stream__school", label="School")
    school_emis_code = django_filters.NumberFilter(field_name="stream__school__emis_code", label="School Emis Code", lookup_expr="icontains")
    school_sub_county = django_filters.NumberFilter(field_name="stream__school__sub_county_id", label="School Sub County Id")
    school_county = django_filters.NumberFilter(field_name="stream__school__sub_county__county_id", label="School County Id")

    year = django_filters.NumberFilter(field_name="date__year", label="Year")
    month = django_filters.NumberFilter(field_name="date__month", label="Month")
    special_needs = django_filters.NumberFilter(field_name="student__special_needs", label="Special Needs")
    is_training_school = django_filters.BooleanFilter(field_name="stream__school__is_training_school")
    partner = django_filters.NumberFilter( label="Partner Id", method="filter_partner")
    # has_special_needs=django_filters.BooleanFilter(method="filter_has_special_need", label="Has Special Need")
    no_special_needs=django_filters.BooleanFilter(field_name="student__special_needs", label="Has Special Need",lookup_expr="isnull")
    
    
    # partner=django_filters.NumberFilter(name="partner",method="filter_partner")
    # partner_admin=django_filters.NumberFilter(name="partner",method="filter_partner_admin",label="Partner Admin Id")
    # county_name=django_filters.CharFilter(name="stream__school__zone__subcounty__county__county_name",lookup_expr="icontains")
    # county = django_filters.NumberFilter(name="stream__school__zone__subcounty__county_id", label="County Id")

    # date_range = django_filters.DateRangeFilter(name='date')
    class Meta:
        model = Attendance
        fields = "__all__" 
    
    def filter_has_special_need(self,queryset,name,value):
        
        # print("The value is ",value)
        
        queryset = queryset.annotate(special_needs_count=Count("student__special_needs")) 
        
        # print(queryset.values("special_needs_count")[0])
        
        if value:
            
            return queryset.filter(special_needs_count__gt=0)
            
        return queryset.filter(special_needs_count=0)

    def filter_partner(self, queryset, name, value):
        # return queryset.filter(stream__school__partners__id=value)
        if value==None:
            return queryset
        if not User.objects.filter(id=value).exists():
            raise my_common.MyCustomException(400,"Partner does not exist.")
        return my_common.filter_queryset_based_on_role(queryset,value)
    

    def filter_is_oosc(self, queryset, name, value):
        return queryset.filter(student__is_oosc=str2bool(value))

    def filter_partner_admin(self, queryset, name, value):
        return queryset.filter(stream__school__partners__partner_admins__id=value)
