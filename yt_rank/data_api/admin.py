from django.contrib import admin

# Register your models here.
from .models import ThreadInfoData,UpdateInfoData

class AdminUpdateInfo(admin.ModelAdmin):
    model = UpdateInfoData
    list_display = (
        'anydesk_id',
        'host_name',
        'uuid',
        'task_type',
        'try_done',
        'success',
        'msg',
        'process_name',
        'target_path',
        'file_name',
        'line_from',
        'line_to',
        'absolute_path',
        'download_url',
        'after_run',
    )
    list_filter = ['success']

admin.site.register(UpdateInfoData,AdminUpdateInfo)

class AdminThreadInfo(admin.ModelAdmin):
    model = ThreadInfoData
    list_display = (
        'anydesk_id',
        'server_num',
        # 'host_name',

        # 'hai_ip_account',
        # 'total_logged_in',
        'thread_index',
        'google_logged_in',
        'now_state',
        'target_state',
        'rank',


        # 'user_agent',

        'keyword',
        'is_filter',
        'target_url',
        'enter_type',

        'google_id',
        'google_password',
        'google_email',
        'proxy',
        'last_connected_timestamp'
    )
    list_filter = ['google_logged_in']

admin.site.register(ThreadInfoData,AdminThreadInfo)

