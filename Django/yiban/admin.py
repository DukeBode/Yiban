from django.contrib import admin

# Register your models here.
from .models import User

admin.site.site_header = '易班系统'
admin.site.site_title = '管理中心'
admin.site.index_title = '后台管理'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid','username','sex','schoolname')
