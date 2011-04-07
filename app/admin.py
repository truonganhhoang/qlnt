from app.models import TimeTable
from app.models import SystemDataType, UserTypeDataType
#from app.models import MarkByPeriod, SysValueMarkType
from django.contrib import admin

admin.site.register(TimeTable)
admin.site.register(SystemDataType)
admin.site.register(UserTypeDataType)
#admin.site.register(MarkByPeriod)
#admin.site.register(SysValueMarkType)