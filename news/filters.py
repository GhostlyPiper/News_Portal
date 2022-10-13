from django.forms import DateInput

from django_filters import (FilterSet,
                            ModelChoiceFilter,
                            ModelMultipleChoiceFilter,
                            DateFilter,
                            CharFilter,
                            )

from .models import Author, Category, CategorySubscribers


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label='Опубликовано после',
        widget=DateInput(attrs={'type': 'date'})
    )
    title = CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит'
    )
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все'
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
        label='Категория',
    )


class CategoryFilter(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())
    user = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = CategorySubscribers
        fields = ['category']
