from django.contrib import admin

from .models import (
                    Author,
                    Category,
                    Post,
                    Comment,
                    CategorySubscribers,
                    PostCategory,
                    # AuthorSubscribers,
                    )


def nullify_rating(modeladmin, request, queryset):
    """ Обнуляет рейтинг выбранных постов """
    # все аргументы уже знакомы, самые нужные из них это
    # request — объект хранящий информацию о запросе и
    # queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
    nullify_rating.short_description = 'Сделать рейтинг нулевым'


def nullify_rating_author(modeladmin, request, queryset):
    """ Обнуляет рейтинг выбранных постов """
    # все аргументы уже знакомы, самые нужные из них это
    # request — объект хранящий информацию о запросе и
    # queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(ratingAuthor=0)
    nullify_rating_author.short_description = 'Сделать рейтинг нулевым'


# создаём новый класс для представления постов в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями,
    # которые вы хотите видеть в таблице
    list_display = ('title', 'author', 'dateCreation', 'text', 'rating')
    list_filter = ('rating', 'dateCreation', 'author')
    search_fields = ('title', 'postCategory__name')
    actions = [nullify_rating]


class AuthorAdmin(admin.ModelAdmin):  # TranslationAdmin):

    model = Author
    list_display = ('authorUser', 'ratingAuthor',)
    list_filter = ('ratingAuthor',)
    search_fields = ('authorUser', 'ratingAuthor',)
    actions = [nullify_rating_author]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)
admin.site.register(PostCategory)
