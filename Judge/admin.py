from django.contrib import admin
from .models import EmailContent, EmailUser
# Register your models here.

admin.site.site_title = "邮件系统"
admin.site.site_header = "邮件系统"
admin.site.index_title = "邮件系统"

admin.site.register([EmailContent, EmailUser])
