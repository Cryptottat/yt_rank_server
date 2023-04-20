from django.db import models

# Create your models here.
class ThreadInfo(models.Model):

    host_name = models.CharField(max_length=20, null=False)
    anydesk_id = models.CharField(max_length=20, null=False)
    hai_ip_account = models.CharField(max_length=20, null=False)
    total_logged_in = models.IntegerField(null=False, default=0)
    thread_index = models.IntegerField(null=False)
    server_num = models.IntegerField(null=True, default=None)
    proxy = models.CharField(max_length=20, null=True, default=None)
    google_id = models.CharField(max_length=50, null=True, default=None)
    google_password = models.CharField(max_length=50, null=True, default=None)
    google_email = models.CharField(max_length=50, null=True, default=None)
    user_agent = models.CharField(max_length=200, null=True, default=None)
    google_logged_in = models.BooleanField(null=False, default=False)
    keyword = models.CharField(max_length=100, null=True, default=None)
    is_filter = models.BooleanField(null=False, default=False)
    target_url = models.CharField(max_length=200, null=True, default=None)
    enter_type = models.CharField(max_length=20, null=True, default=None)
    now_state = models.CharField(max_length=20, null=True, default=None)
    target_state = models.CharField(max_length=20, null=True, default=None)
    last_connected_timestamp = models.BigIntegerField(null=True, default=None)
    class Meta:
        db_table = 'thread_data'
        verbose_name = '스레드 테이블'