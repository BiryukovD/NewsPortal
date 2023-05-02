from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail, EmailMessage
from django.http import request
from django.template.loader import render_to_string

from .models import *


@receiver(m2m_changed, sender=Post.category.through)
def post_handler(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories_new_post = Category.objects.filter(post=instance.id)
        email_list = []
        for category in categories_new_post:
            subscribers_of_category = Subscriber.objects.filter(category=category.pk)

            if subscribers_of_category.exists():
                for subscriber in subscribers_of_category:
                    user = User.objects.get(pk=subscriber.user_id)
                    email_list.append(user.email)

        email_set = set(email_list)
        email_list_unique = list(email_set)

        title = instance.title
        content = instance.content

        subject, from_email, to = 'В вашей любимой категории новая статья!', 'dim.bir2017@yandex.ru', email_list_unique
        html_content = render_to_string('new_post_in_category.html',
                                        {'title': title, 'content': content, 'instance': instance})

        msg = EmailMessage(subject, html_content, from_email, to)
        msg.content_subtype = "html"
        msg.send()







