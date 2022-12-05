from .models import Category, Post, Comment

# импортируем декоратор для перевода и класс настроек,
# от которого наследоваться
from modeltranslation.translator import register, TranslationOptions


# регистрируем модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # какие поля надо переводить


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('text',)
