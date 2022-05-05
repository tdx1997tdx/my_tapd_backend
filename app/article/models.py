from django.db import models
from app.user.models import User


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_public = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
