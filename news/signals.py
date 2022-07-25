import os

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta, date


@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postCategory.all():
            for subscribe in CategorySubscribers.objects.filter(category=cat):
                message = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.text,
                    from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                    to=[subscribe.user.email],
                )

                html_content = render_to_string(
                    'post_created.html',
                    {
                        'post': instance,
                        'recipient': subscribe.user.email,
                        'name': subscribe.user

                    }
                )

                message.attach_alternative(html_content, "text/html")
                message.send()


def collect_subscribers(category):
    """ Перебрать всех подписчиков в таблице категорий, извлечь их электронную почту
     и сформировать список получателей электронной почты """
    email_recipients = []
    for user in category.subscribers.all():
        email_recipients.append(user.email)
    return email_recipients


def send_emails(post_object, *args, **kwargs):
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
    )

    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email=os.getenv('DEFAULT_FROM_EMAIL'),
        to=kwargs['email_recipients']  # отправляем всем из списка
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)


def week_post_2():
    """ Функция отправки рассылки подписчикам за неделю """
    week = timedelta(days=1)
    posts = Post.objects.all()
    past_week_posts = []
    template = 'weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for post in posts:
        time_delta = date.today() - post.create_date.date()
        if time_delta < week:
            past_week_posts.append(post)

    past_week_categories = set()
    for post in past_week_posts:

        for category in post.post_category.all():
            past_week_categories.add(category)

    email_recipients_set = set()
    for category in past_week_categories:
        # запрос почтового ящика пользователя
        get_user_emails = set(collect_subscribers(category))
        email_recipients_set.update(get_user_emails)
    email_recipients = list(email_recipients_set)

    for email in email_recipients:
        post_object = []
        categories = set()

        for post in past_week_posts:
            subscription = post.post_category.all().values('subscribers').filter(subscribers__email=email)

            if subscription.exists():
                post_object.append(post)
                categories.update(post.post_category.filter(subscribers__email=email))

        category_object = list(categories)

        send_emails(
            post_object,
            category_object=category_object,
            email_subject=email_subject,
            template=template,
            email_recipients=[email, ]
        )
