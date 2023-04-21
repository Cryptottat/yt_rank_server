from django.db import models


# Create your models here.
class ThreadInfoData(models.Model):
    host_name = models.CharField(max_length=20, null=False, verbose_name="컴터ID")
    anydesk_id = models.CharField(max_length=20, null=False, verbose_name=u"애니데스크")
    hai_ip_account = models.CharField(max_length=20, null=False, verbose_name=u"Hai-IP")
    total_logged_in = models.IntegerField(null=False, default=0, verbose_name=u"총로긴")
    thread_index = models.IntegerField(null=False, verbose_name=u"스레드")
    server_num = models.IntegerField(null=True, default=None, verbose_name=u"서버")
    proxy = models.CharField(max_length=20, null=True, default=None, verbose_name=u"프록시")
    google_id = models.CharField(max_length=50, null=True, default=None, verbose_name=u"ID")
    google_password = models.CharField(max_length=50, null=True, default=None, verbose_name=u"PASS")
    google_email = models.CharField(max_length=50, null=True, default=None, verbose_name=u"Email")
    user_agent = models.CharField(max_length=200, null=True, default=None, verbose_name=u"U-agent")
    google_logged_in = models.BooleanField(null=False, default=False, verbose_name=u"Lg")
    rank = models.IntegerField(null=True, default=999, verbose_name=u"순위")
    keyword = models.CharField(max_length=100, null=True, balnk=True, default=None, verbose_name=u"검색어")
    is_filter = models.BooleanField(null=False, default=False, verbose_name=u"실시간")
    target_url = models.CharField(max_length=200, balnk=True, null=True, default=None, verbose_name=u"타겟 주소")
    enter_type = models.CharField(max_length=20, balnk=True, null=True, default=None, verbose_name=u"진입 방법")
    now_state = models.CharField(max_length=20, balnk=True, null=True, default=None, verbose_name=u"상태")
    target_state = models.CharField(max_length=20, balnk=True, null=True, default=None, verbose_name=u"명령")
    last_connected_timestamp = models.BigIntegerField(null=True, default=0, verbose_name=u"마지막 접속")

    class Meta:
        db_table = 'thread_info_data_table'
        verbose_name = u'Thread Info Data'
