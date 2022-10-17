from celery import shared_task
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, CategorySubscribers
from NewsPaper import settings


def send_notifications(preview, pk, title, subscribe):
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'text': preview,
            'link': f"{settings.SITE_URL}/news/{pk}",
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscribe.user.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def notify_news_create(oid):
    new_post = Post.objects.get(pk=oid)

    for cat in new_post.postCategory.all():
        for subscribe in CategorySubscribers.objects.filter(category=cat):

            send_notifications(
                new_post.preview(),
                new_post.pk,
                new_post.title,
                subscribe
            )


@shared_task
def weekly_mailing():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'news/weekly_digest.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
