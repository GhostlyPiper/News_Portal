from django.forms import DateInput

from django_filters import (FilterSet,
                            ModelChoiceFilter,
                            ModelMultipleChoiceFilter,
                            DateFilter,
                            CharFilter,
                            )

from .models import Post, Author, Category, CategorySubscribers
from django.utils.translation import gettext_lazy as _


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label=_('Published after'),
        widget=DateInput(attrs={'type': 'date'})
    )
    title = CharFilter(
        lookup_expr='icontains',
        label=_('The header contains')
    )
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label=_('Author'),
        empty_label=_('All')
    )
    date.field.error_messages = {
        'invalid': 'Enter date in format DD.MM.YYYY. Example: 31.12.2020'
    }
    date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}
    # Этот вариант не самый удачный!
    # Category = ModelChoiceFilter(
    #     field_name='postCategory',
    #     queryset=Category.objects.all(),
    #     label='Категория',
    #     empty_label='Любая'
    # )

    Category = ModelMultipleChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label=_('Category'),
    )


class CategoryFilter(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())
    user = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = CategorySubscribers
        fields = ['category']
