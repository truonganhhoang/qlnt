from app.models import TimeTable
from app.models import SystemDataType, UserTypeDataType
from django.contrib import admin

admin.site.register(TimeTable)
admin.site.register(SystemDataType)
admin.site.register(UserTypeDataType)
