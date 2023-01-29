from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# createing Model manager to retrive all PUBLISHED Posts 
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
        

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF',   'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    # unique_for_date slug to be different for oublication date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # default model manager
    objects= models.Manager()
    #custom managery
    published = PublishedManager()
    # django-taggit
    tags = TaggableManager()

    # metadata for the model 
    # ordering attr tells django  to sort result by published field
    class Meta:
        ordering = ['-publish']
        # database index to improve query filter performance
        indexes = [
            models.Index(fields=['-publish'])
        ]

    # str method returns a string with human-readable representation of the object
    def __str__(self):
        return self.title

    # using canonical Url for models
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month,self.publish.day, self.slug])   


# comments Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'