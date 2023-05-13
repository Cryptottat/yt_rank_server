from django.contrib import admin
from .models import User,TelegramInfo
# Register your models here.


class AdminUser(admin.ModelAdmin):
    model = User
    list_display = (
        'username',
        'email',
        'point',
    )

class AdminTelegramInfo(admin.ModelAdmin):
    model = TelegramInfo

# Register your models here.
admin.site.register(User,AdminUser)
admin.site.register(TelegramInfo,AdminTelegramInfo)
