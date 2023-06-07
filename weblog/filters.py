from django_filters import rest_framework as rf
from rest_framework import filters

from .models import Post

class DateFilter(rf.FilterSet, filters.OrderingFilter):
    date = rf.DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['date']