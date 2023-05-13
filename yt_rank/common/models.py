# models.py

from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=30,null=False,default='',unique=True)
    point = models.IntegerField(null=False,default=0)
    # class Meta:
    #     unique_together = ('username', 'email')

class TelegramInfo(models.Model):
    bot_token = models.CharField(max_length=100, verbose_name='봇 토큰')
    chat_id = models.CharField(max_length=30, verbose_name='챗 ID')