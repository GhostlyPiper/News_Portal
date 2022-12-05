from django.contrib import admin

from .models import (
                    Author,
                    Category,
                    Post,
                    Comment,
                    CategorySubscribers,
                    PostCategory,
                    )

# импортируем модель амдинки
from modeltranslation.admin import TranslationAdmin


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
class PostAdmin(TranslationAdmin):  # admin.ModelAdmin
    # list_display — это список или кортеж со всеми полями,
    # которые вы хотите видеть в таблице
    model = Post
    list_display = ('title', 'author', 'dateCreation', 'text', 'rating')
    list_filter = ('rating', 'dateCreation', 'author')
    search_fields = ('title', 'postCategory__name')
    list_per_page = 5
    actions = [nullify_rating]


class AuthorAdmin(admin.ModelAdmin):  # TranslationAdmin):

    model = Author
    list_display = ('authorUser', 'ratingAuthor',)
    list_filter = ('ratingAuthor',)
    search_fields = ('authorUser', 'ratingAuthor',)
    actions = [nullify_rating_author]


class CategoryAdmin(TranslationAdmin):  # admin.ModelAdmin):
    model = Category


class CommentAdmin(TranslationAdmin):  # admin.ModelAdmin):
    model = Comment


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CategorySubscribers)
admin.site.register(PostCategory)
