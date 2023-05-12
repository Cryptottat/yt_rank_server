from django.contrib import admin

# Register your models here.
from .models import Announcement,PricePerHour,Order

class AdminAnnouncement(admin.ModelAdmin):
    model = Announcement
    list_display = (
        'subject',
        'create_date',
    )
# Register your models here.

class AdminPricePerHour(admin.ModelAdmin):
    model = PricePerHour
    # list_display = (
    #     'subject',
    #     'create_date',
    # )
# Register your models here.

# Register your models here.
class AdminOrder(admin.ModelAdmin):
    model = Order
    list_display = (
        'username',
        'target_time',
        'keyword',
        'target_url',
        'charge',
        'order_time',
    )
# Register your models here.
admin.site.register(Announcement,AdminAnnouncement)
admin.site.register(PricePerHour,AdminPricePerHour)
admin.site.register(Order,AdminOrder)

