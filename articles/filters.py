import  django_filters
from .models import Articles, Category

class ArticlesFilter( django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')  # Case-insensitive title search

    class Meta:
        model = Articles
        fields = ['title']