from django.db import models

from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token
from common.models import User

# class M_User(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.OneToOneField(User, on_delete=models.CASCADE)
# class MultiToken(Token):
#     user = models.ForeignKey(  # changed from OneToOne to ForeignKey
#         settings.AUTH_USER_MODEL, related_name='tokens',
#         on_delete=models.CASCADE, verbose_name=("User")
#     )
#     pass

class PointValue(models.Model):
    point_price = models.FloatField()

class TokenPoint(models.Model):
    key = models.OneToOneField(Token, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    status = models.CharField(default='',max_length=20)
