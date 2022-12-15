from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(
            commentRating=Sum('rating')
        )
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat*3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Category(models.Model):
    name = models.CharField(max_length=64,
                            help_text=_('category name'),
                            unique=True
                            )
    subscribers = models.ManyToManyField(
        User,
        through='CategorySubscribers',
        blank=True,
        verbose_name=_('subscribers'),
    )

    def __str__(self):
        return f'{self.name.title()}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class CategorySubscribers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.user} <->  {self.category}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, _('News')),
        (ARTICLE, _('Article')),
    )
    categoryType = models.CharField(max_length=2,
                                    choices=CATEGORY_CHOICES,
                                    default=ARTICLE
                                    )
    dateCreation = models.DateTimeField(default=timezone.now)
    postCategory = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name=_('category'),
    )
    title = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('title'),
    )
    text = models.TextField(
        verbose_name=_('text'),
    )
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        # сначала вызываем метод родителя, чтобы объект сохранился
        super().save(*args, **kwargs)
        # затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.postThrough} <-> {self.categoryThrough}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
