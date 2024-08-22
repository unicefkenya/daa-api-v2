import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet

from client.models import MyUser


class UsersFilter(FilterSet):
    search = django_filters.CharFilter(label="General Search", method="filter_name")

    class Meta:
        model = MyUser
        fields = "__all__"
        exclude = ("image",)

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(username__icontains=value.upper()) | Q(first_name__icontains=value) | Q(last_name__icontains=value))
