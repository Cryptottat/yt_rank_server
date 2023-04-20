from django.db import models

# Create your models here.
class ThreadInfo(models.Model):

    host_name = models.CharField(max_length=20, null=False, verbose_name="컴터ID")
    anydesk_id = models.CharField(max_length=20, null=False, verbose_name="애니데스크")
    hai_ip_account = models.CharField(max_length=20, null=False, verbose_name="Hai-IP")
    total_logged_in = models.IntegerField(null=False, default=0, verbose_name="총로긴")
    thread_index = models.IntegerField(null=False, verbose_name="스레드")
    server_num = models.IntegerField(null=True, default=None, verbose_name="서버")
    proxy = models.CharField(max_length=20, null=True, default=None, verbose_name="프록시")
    google_id = models.CharField(max_length=50, null=True, default=None, verbose_name="ID")
    google_password = models.CharField(max_length=50, null=True, default=None, verbose_name="PASS")
    google_email = models.CharField(max_length=50, null=True, default=None, verbose_name="Email")
    user_agent = models.CharField(max_length=200, null=True, default=None, verbose_name="U-agent")
    google_logged_in = models.BooleanField(null=False, default=False, verbose_name="Lg")
    keyword = models.CharField(max_length=100, null=True, default=None, verbose_name="검색어")
    is_filter = models.BooleanField(null=False, default=False, verbose_name="실시간")
    target_url = models.CharField(max_length=200, null=True, default=None, verbose_name="타겟 주소")
    enter_type = models.CharField(max_length=20, null=True, default=None, verbose_name="진입 방법")
    now_state = models.CharField(max_length=20, null=True, default=None, verbose_name="상태")
    target_state = models.CharField(max_length=20, null=True, default=None, verbose_name="명령")
    last_connected_timestamp = models.BigIntegerField(null=True, default=None, verbose_name="마지막 접속")
    class Meta:
        db_table = 'thread_data'
        verbose_name = 'Thread Info'