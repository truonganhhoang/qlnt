from django.contrib import admin
from app.models import Organization, User, PositionType, SchoolYear, Semester

#admin.site.register(School)
admin.site.register(Organization)
admin.site.register(PositionType)
admin.site.register(User)
admin.site.register(SchoolYear)
admin.site.register(Semester)