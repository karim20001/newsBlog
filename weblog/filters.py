from django_filters import rest_framework as rf

from .models import Post

class DateFilter(rf.FilterSet):
    date = rf.DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['date']