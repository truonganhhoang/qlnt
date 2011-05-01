from django.contrib import admin
from app.models import Organization, UserProfile, Position
#, SchoolYear, Semester

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'upper_organization', 'manager_name')
    list_filter = ('level', 'upper_organization', 'name')
    search_fields = ['name', 'email', 'manager_name']
    list_editable = ['name', 'address', 'email', 'upper_organization', 'manager_name']
    list_per_page = 20
            
admin.site.register(Organization, OrganizationAdmin)

admin.site.register(Position)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'birthday', 'email', 'phone', 'organization')
    list_filter = ('organization')
    search_fields = ['name', 'email']
admin.site.register(UserProfile)


#admin.site.register(School)
#admin.site.register(SchoolYear)
#admin.site.register(Semester)