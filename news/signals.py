import os

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_notifications(preview, pk, title, subscribe):
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'text': preview,
            'link': f"{os.getenv('SITE_URL')}/news/{pk}",
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=os.getenv('DEFAULT_FROM_EMAIL'),
        to=[subscribe.user.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# @receiver(m2m_changed, sender=PostCategory)  # Если раскоментировать по сигналу будет уходить емаил
# def notify_news_create(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         for cat in instance.postCategory.all():
#             for subscribe in CategorySubscribers.objects.filter(category=cat):
#
#                 send_notifications(
#                     instance.preview(),
#                     instance.pk,
#                     instance.title,
#                     subscribe
#                 )
