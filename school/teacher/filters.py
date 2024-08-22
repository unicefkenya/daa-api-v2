import django_filters
from django.db.models import Q

from django_filters.rest_framework import FilterSet

from school.models import Teacher


class TeacherFilter(FilterSet):
    school = django_filters.NumberFilter(field_name="school", label="School Id")
    school_emis_code = django_filters.NumberFilter(field_name="school__emis_code", label="School emis code")
    name = django_filters.CharFilter(method="filter_students_by_names", label="Any Student Name")
    first_name=django_filters.CharFilter(lookup_expr="icontains")
    middle_name=django_filters.CharFilter(lookup_expr="icontains")
    last_name=django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model=Teacher
        fields=("__all__")


    def filter_students_by_names(self,queryset,name, value):
        names = value.split(" ")
        if len(names) > 2:
            return queryset.filter(
                Q(first_name__icontains=names[0]), Q(middle_name__icontains=names[1]), Q(last_name__icontains=names[2]))
        elif len(names) == 2:
            return queryset.filter(
                Q(first_name__icontains=names[0]),
                (Q(last_name__icontains=names[1]) | Q(middle_name__icontains=names[1])))

        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(middle_name__icontains=value)
        )