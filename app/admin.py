from django.contrib import admin
from app.models import MarkByPeriod, UserTypeDataType, TimeTable, SystemDataType

#admin.site.register(School)
admin.site.register(TimeTable)
admin.site.register(SystemDataType)
admin.site.register(UserTypeDataType)
admin.site.register(MarkByPeriod)
#admin.site.register(SysValueMarkType)