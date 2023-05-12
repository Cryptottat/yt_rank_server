from django.contrib import admin

# Register your models here.

from .models import PointValue,TokenPoint

class AdminPointValue(admin.ModelAdmin):
    model = PointValue
    # list_display = (
    #     'subject',
    #     'create_date',
    # )
class AdminTokenPoint(admin.ModelAdmin):
    model = TokenPoint

# Register your models here.


# Register your models here.
admin.site.register(PointValue,AdminPointValue)
admin.site.register(TokenPoint,AdminTokenPoint)

