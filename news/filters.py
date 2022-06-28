from django.forms import DateInput

from django_filters import (FilterSet,
                            ModelChoiceFilter,
                            DateFilter,
                            CharFilter,
                            )

from .models import Post, Author


class PostFilter(FilterSet):
    date = DateFilter(field_name='dateCreation',
                      lookup_expr='gte',
                      label='Create after',
                      widget=DateInput(attrs={'type': 'date'}))
    title = CharFilter(lookup_expr='icontains')
    author = ModelChoiceFilter(queryset=Author.objects.all())
    date.field.error_messages = {'invalid': 'Enter date in format DD.MM.YYYY. Example: 31.12.2020'}
    date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}

    class Meta:
        model = Post
        fields = ['date', 'title', 'author']

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }
