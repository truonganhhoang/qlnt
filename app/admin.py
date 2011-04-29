from django.contrib import admin
from app.models import Organization, User, PositionType
#, SchoolYear, Semester

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'upper_organization', 'manager_name')
    description = "asfasd "

admin.site.register(Organization, OrganizationAdmin)

admin.site.register(PositionType)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'birthday', 'email', 'phone_number', 'organization')
admin.site.register(User)


#admin.site.register(School)
#admin.site.register(SchoolYear)
#admin.site.register(Semester)