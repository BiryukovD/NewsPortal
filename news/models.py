from django.contrib.auth.models import User
from django.db import models
TYPE_POST_CHOICES = [
    ('NEWS', 'NEWS'),
    ('ARCICLE', 'ARTICLE')
]


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


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


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
