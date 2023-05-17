import datetime
from django.core.mail import EmailMessage
from celery import shared_task
import time
from django.template.loader import render_to_string
from .models import *


@shared_task
def hello():
    #time.sleep(10)
    print('Второй')


@shared_task
def send_to_subscriber_new_posts_for_week_in_category():
    past_date = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    all_categories = Category.objects.all()

    for category in all_categories:
        email_list = []
        posts = Post.objects.filter(time_in__gte=past_date, category=category)
        subscribers_of_category = Subscriber.objects.filter(category=category)
        if subscribers_of_category.exists():
            for subscriber in subscribers_of_category:
                user = User.objects.get(pk=subscriber.user_id)
                email_list.append(user.email)

            subject, from_email, to = f'Список новых статей в вашей любимой категории({category}) за неделю!', 'dim.bir2017@yandex.ru', email_list
            html_content = render_to_string('new_posts_in_category_for_week.html', {'posts': posts})
            msg = EmailMessage(subject, html_content, from_email, to)
            msg.content_subtype = "html"
            msg.send()


@shared_task()
def send_to_subscriber_new_post_in_category(instance_id):
    instance = Post.objects.get(id=instance_id)
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
