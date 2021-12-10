from django.contrib import admin
from .models import *
# Register your models here.


class UserAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'doing_name', 'doing_type', 'doing', 'doing_date', 'username')


admin.site.register(UserProfile)
admin.site.register(GroupProfile)
admin.site.register(Departments)
admin.site.register(Permission)
admin.site.register(Servers)
admin.site.register(ServerPassword)
admin.site.register(UserAudit, UserAuditAdmin)

