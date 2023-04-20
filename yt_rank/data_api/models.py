from django.db import models


# Create your models here.
class ThreadInfoData(models.Model):
    host_name = models.CharField(max_length=20, null=False, verbose_name="Com ID")
    anydesk_id = models.CharField(max_length=20, null=False, verbose_name="AnyDesk")
    hai_ip_account = models.CharField(max_length=20, null=False, verbose_name="Hai-IP")
    total_logged_in = models.IntegerField(null=False, default=0, verbose_name="Togin")
    thread_index = models.IntegerField(null=False, verbose_name="Thread")
    server_num = models.IntegerField(null=True, default=None, verbose_name="Server")
    proxy = models.CharField(max_length=20, null=True, default=None, verbose_name="Proxy")
    google_id = models.CharField(max_length=50, null=True, default=None, verbose_name="ID")
    google_password = models.CharField(max_length=50, null=True, default=None, verbose_name="PASS")
    google_email = models.CharField(max_length=50, null=True, default=None, verbose_name="Email")
    user_agent = models.CharField(max_length=200, null=True, default=None, verbose_name="U-agent")
    google_logged_in = models.BooleanField(null=False, default=False, verbose_name="Login")
    keyword = models.CharField(max_length=100, null=True, default=None, verbose_name="KeyWord")
    is_filter = models.BooleanField(null=False, default=False, verbose_name="Live")
    target_url = models.CharField(max_length=200, null=True, default=None, verbose_name="Target")
    enter_type = models.CharField(max_length=20, null=True, default=None, verbose_name="Enter")
    now_state = models.CharField(max_length=20, null=True, default=None, verbose_name="State")
    target_state = models.CharField(max_length=20, null=True, default=None, verbose_name="Order")
    last_connected_timestamp = models.BigIntegerField(null=True, default=None, verbose_name="Last Connect")

    class Meta:
        db_table = 'thread_info_data_table'
        verbose_name = u'Thread Info Data'
