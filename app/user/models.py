from django.db import models
import datetime


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, null=False)
    nickname = models.CharField(max_length=20)
    introduction = models.CharField(max_length=500)
    birthday = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=50)
    fail_time = models.DateTimeField(
        default=(datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"))
