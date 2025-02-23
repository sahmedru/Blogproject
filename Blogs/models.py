from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class categories(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name
    
class tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name
    
class posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(categories, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.ManyToManyField(tags, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    view_count = models.PositiveBigIntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_posts')
    def __str__(self):
        return self.title
    
class comments(models.Model):
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content