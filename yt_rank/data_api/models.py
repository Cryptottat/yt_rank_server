from django.db import models


# Create your models here.
class UpdateInfoData(models.Model):
    anydesk_id = models.CharField(max_length=20, null=False, verbose_name=u"애니데스크")
    excel_num = models.IntegerField(null=True, blank=True, default=None, verbose_name=u"엑셀")
    host_name = models.CharField(max_length=50, default=None, null=True, verbose_name="컴터ID")
    uuid = models.CharField(max_length=50, null=False, verbose_name=u"UUID")
    task_type = models.CharField(max_length=20, null=False, verbose_name=u"수행타입")
    try_done = models.BooleanField(null=False, blank=False, default=False, verbose_name=u"수행시도")
    success = models.BooleanField(null=True, blank=True, default=None, verbose_name=u"성공/실패")
    msg = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"(에러)메시지")
    target_path = models.CharField(max_length=300, null=True, blank=True,default=None, verbose_name=u"경로(또는폴더경로)")
    file_name = models.CharField(max_length=300, null=True, blank=True,default=None, verbose_name=u"파일명")
    download_url = models.CharField(max_length=300, null=True, blank=True, default=None, verbose_name=u"다운로드 주소")
    line_from = models.IntegerField(null=True, blank=True, default=None, verbose_name=u"부터")
    line_to = models.IntegerField(null=True, blank=True, default=None, verbose_name=u"까지")
    absolute_path = models.BooleanField(null=True, blank=True, default=None, verbose_name=u"절대경로여부")
    after_run = models.BooleanField(null=True, blank=True, default=None, verbose_name=u"다운로드 후 실행 여부")
    process_name = models.CharField(max_length=300, null=True, blank=True, default=None, verbose_name=u"프로세스명")

class ThreadInfoData(models.Model):
    excel_num = models.IntegerField(null=True, blank=True, default=None, verbose_name=u"엑셀")
    host_name = models.CharField(max_length=20, null=True, verbose_name="컴터ID")
    anydesk_id = models.CharField(max_length=20, null=False, verbose_name=u"애니데스크")
    hai_ip_account = models.CharField(max_length=20, null=False, verbose_name=u"Hai-IP")
    total_logged_in = models.IntegerField(null=True, blank=True, default=None, verbose_name=u"총로긴")
    thread_index = models.IntegerField(null=False, verbose_name=u"스레드")
    chrome = models.BooleanField(null=True,blank=True,default=None,verbose_name=u"크롬창")
    server_num = models.IntegerField(null=True, blank=True, default=None, verbose_name=u"서버")
    proxy = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name=u"프록시")
    google_id = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name=u"ID")
    google_password = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name=u"PASS")
    google_email = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name=u"Email")
    user_agent = models.CharField(max_length=200, null=True, blank=True, default=None, verbose_name=u"U-agent")
    google_logged_in = models.BooleanField(null=True, blank=True, default=None, verbose_name=u"Lg")
    rank = models.IntegerField(null=True, blank=True, default=999, verbose_name=u"순위")
    keyword = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name=u"검색어")
    is_filter = models.BooleanField(null=False, blank=True, default=False, verbose_name=u"실시간")
    target_url = models.CharField(max_length=200, blank=True, null=True, default=None, verbose_name=u"타겟 주소")
    enter_type = models.CharField(max_length=20, blank=True, null=True, default=None, verbose_name=u"진입 방법")
    now_state = models.CharField(max_length=20, blank=True, null=True, default=None, verbose_name=u"상태")
    target_state = models.CharField(max_length=20, blank=True, null=True, default=None, verbose_name=u"명령")
    last_connected_timestamp = models.CharField(max_length=25,null=True, blank=True, default=0, verbose_name=u"마지막 접속")
    state_for_main = models.CharField(max_length=25,null=True, blank=True, default=None, verbose_name=u"메인 제어용")

    class Meta:
        db_table = 'thread_info_data_table'
        verbose_name = u'Thread Info Data'
