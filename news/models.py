from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.sites.models import Site


TYPE_POST_CHOICES = [
    ('NEWS', 'NEWS'),
    ('ARCICLE', 'ARTICLE')
]


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        list_of_posts_by_author = Post.objects.filter(author_id=self.pk)
        list_comments_by_author = Comment.objects.filter(user_id=self.user_id)
        points_for_posts = 0
        points_for_comments_by_author = 0
        points_for_comments_to_posts_by_author = 0
        for post in list_of_posts_by_author:
            points_for_posts += post.rating
        for comment in list_comments_by_author:
            points_for_comments_by_author += comment.rating
        for post in list_of_posts_by_author:
            comments = Comment.objects.filter(post_id=post.pk)
            for comment in comments:
                points_for_comments_to_posts_by_author += comment.rating
        rating_of_author = (points_for_posts * 3) + points_for_comments_by_author + points_for_comments_to_posts_by_author
        self.rating = rating_of_author
        self.save()
    def __str__(self):
        return f'{User.objects.get(pk = self.user_id)}'


class Post(models.Model):
    category = models.ManyToManyField(Category, through='PostCategory')
    type = models.CharField(max_length=64, choices=TYPE_POST_CHOICES)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64, blank=True)
    content = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        rating = self.rating
        added = rating + 1
        self.rating = added
        self.save()

    def dislike(self):
        rating = self.rating
        added = rating - 1
        self.rating = added
        self.save()

    def preview(self):
        preview = self.content
        return preview[:124] + '...'
    def __str__(self):
        return f'{self.title} {self.time_in} {self.content[:20]}...'

    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        return 'http://127.0.0.1:8000' + reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    text = models.CharField(max_length=64)
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        rating = self.rating
        added = rating + 1
        self.rating = added
        self.save()

    def dislike(self):
        rating = self.rating
        added = rating - 1
        self.rating = added
        self.save()

    def __str__(self):
        return f'{self.text}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.post} - {self.category}'

class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    def __str__(self):
        return f'{User.objects.get(pk = self.user_id)}'


