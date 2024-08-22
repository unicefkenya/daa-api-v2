import django_filters
from django.db.models import Q,Count

from school.models import Student
from django_filters.rest_framework import FilterSet
import mylib.my_common as my_common
from django.contrib.auth import get_user_model

User=get_user_model()

class EnrollmentFilter(FilterSet):
    base_class = django_filters.NumberFilter(field_name="stream__base_class", label="Stream Id")
    school = django_filters.NumberFilter(field_name="stream__school_id", label="School Id")
    school_sub_county = django_filters.NumberFilter(field_name="stream__school__sub_county_id", label="School Sub County Id")
    county = django_filters.NumberFilter(field_name="sub_county__county_id", label="Leaner County Id")
    school_county = django_filters.NumberFilter(field_name="stream__school__sub_county__county_id", label="School County Id")
    school_emis_code = django_filters.CharFilter(field_name="stream__school__emis_code", label="School emis code")
    start_date = django_filters.DateFilter(field_name="date_enrolled", lookup_expr=("gte"))
    end_date = django_filters.DateFilter(field_name="date_enrolled", lookup_expr=("lte"))
    year = django_filters.NumberFilter(field_name="date_enrolled", lookup_expr=("year"))
    name = django_filters.CharFilter(method="filter_students_by_names", label="Any Student Name")
    is_training_school = django_filters.BooleanFilter(field_name="stream__school__is_training_school")
    partner = django_filters.NumberFilter( label="Partner Id", method="filter_partner")
    no_special_needs=django_filters.BooleanFilter(field_name="special_needs", label="No Special Need",lookup_expr="isnull")
 
    class Meta:
        model = Student
        exclude = ("moe_extra_info",)
        fields = "__all__"
        
    def filter_has_special_need(self,queryset,name,value):
        # print("The value is ",value)
        queryset=queryset.annotate(special_needs_count=Count("special_needs"))
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
    

    def filter_students_by_names(self, queryset, name, value):
        names = value.split(" ")
        if len(names) > 2:
            return queryset.filter(Q(first_name__icontains=names[0]), Q(middle_name__icontains=names[1]), Q(last_name__icontains=names[2]))
        elif len(names) == 2:
            return queryset.filter(Q(first_name__icontains=names[0]), (Q(last_name__icontains=names[1]) | Q(middle_name__icontains=names[1])))

        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(middle_name__icontains=value))
