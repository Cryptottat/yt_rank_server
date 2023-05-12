from django.db import models


class Announcement(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

class Order(models.Model):
    username = models.CharField(max_length=20,verbose_name="아이디")
    target_time = models.DateTimeField(verbose_name="실행시간")
    keyword = models.CharField(max_length=20,verbose_name="키워드")
    target_url = models.CharField(max_length=200,verbose_name="주소")
    charge = models.IntegerField(verbose_name="몇시간동안")
    order_time = models.DateTimeField(verbose_name="주문시간")

class PricePerHour(models.Model):
    price_per_hour = models.IntegerField()