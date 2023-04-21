from django.contrib import admin

# Register your models here.
from .models import ThreadInfoData

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

admin.site.register(ThreadInfoData,AdminThreadInfo)

