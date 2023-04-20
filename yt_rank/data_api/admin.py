from django.contrib import admin

# Register your models here.
from .models import ThreadInfo

class AdminThreadInfo(admin.ModelAdmin):
    model = ThreadInfo
    list_display = (
        # 'host_name',
        'anydesk_id',
        # 'hai_ip_account',
        # 'total_logged_in',
        'thread_index',
        'google_logged_in',
        'now_state',
        'target_state',
        'server_num',
        'proxy',
        'google_id',
        'google_password',
        'google_email',
        # 'user_agent',

        'keyword',
        'is_filter',
        'target_url',
        'enter_type',
        'last_connected_timestamp'
    )

admin.site.register(ThreadInfo,AdminThreadInfo)

