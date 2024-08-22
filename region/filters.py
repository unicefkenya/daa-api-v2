
import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet

from client.models import MyUser

#
# class PatientFormFilter(FilterSet):
#     start_date=django_filters.DateFilter(field_name="created",lookup_expr="gte")
#     end_date=django_filters.DateFilter(field_name="created",lookup_expr="lte")
#     date=django_filters.DateFilter(field_name="created",lookup_expr="lte")
#     class Meta:
#         model = PatientForm
#         fields = ("__all__")
#         exclude=("image",)
