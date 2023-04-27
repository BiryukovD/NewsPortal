import django_filters
from django.forms import DateInput
from django_filters.widgets import RangeWidget

from django_filters import FilterSet, ModelMultipleChoiceFilter

from .models import Post, Author, Category


class PostFilter(FilterSet):
    title = django_filters.CharFilter(label='Заголовок статьи', lookup_expr='icontains')
    author = ModelMultipleChoiceFilter(queryset=Author.objects.all(), label='Автор', conjoined=True)
    time_in = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), label='Статьи поздее:', lookup_expr='date__gt')
    category = ModelMultipleChoiceFilter(queryset=Category.objects.all(), label='Категория', conjoined=True)

    class Meta:
        model = Post
        fields = ['title', 'author', 'time_in', 'category']
