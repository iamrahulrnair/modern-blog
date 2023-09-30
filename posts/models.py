from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import F

from utils.models import Timestamps
from django.db.models.signals import post_save


class PostManager(models.Manager):
    def create_post(self, title, content, user):
        post = self.create(title=title, content=content, user=user)
        post.save()
        return post

    def update_post(self, title, content, slug, user):
        post = self.get(slug=slug, user=user)
        fields = ['updatedAt', 'slug']
        if title:
            fields.append('title')
            post.title = title
        if content:
            fields.append('content')
            post.content = content
        post.save(update_fields=fields)
        return post

    def delete_post(self, slug, user):
        post = self.get(slug=slug, user=user)
        post.delete()
        return post


class Post(Timestamps, models.Model):
    class Meta:
        ordering = ['-created_at']

    title = models.CharField()
    likes = models.IntegerField(default=0)
    content = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_to_read = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(default="", null=False, db_index=True, unique=True)

    objects = PostManager()

    def save(self, *args, **kwargs):
        """
        Save hook to calculate the total minutes to read the content, took 200 words per minute as an approximation.
        """
        total_words = self.content.split(" ")
        mins = int(len(total_words) * (1 / 200))
        self.time_to_read = mins
        self.slug = slugify(self.title + " " + str(self.time_to_read))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"Post_id: {self.id} - {self.title}"


class PostComment(Timestamps, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_reply_comment = models.BooleanField(default=False)
    replied_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True)


class PostLikes(Timestamps, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


@receiver(post_save, sender=PostLikes)
def add_likes(sender, instance, **kwargs):
    post = instance.post
    post.likes = F('likes') + 1
    post.save()


@receiver(post_save, sender=PostLikes)
def delete_likes(sender, instance, **kwargs):
    post = instance.post
    post.likes = F('likes') - 1
    post.save()
