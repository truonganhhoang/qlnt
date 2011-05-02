from django.contrib import admin
from django.forms.formsets import formset_factory
from app.models import Organization, UserProfile, Position
#, SchoolYear, Semester

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'organization', 'position', 'email', 'phone')
    list_editable = ['first_name', 'last_name', 'organization', 'position', 'email', 'phone']
    list_filter = ('organization')
    search_fields = ['first_name', 'last_name', 'organization',  'email', 'phone', 'notes']
admin.site.register(UserProfile)

class UserProfileInline (admin.StackedInline):
    model = UserProfile
    max_num = 1
   # fk_name =  "organization"
   # fk_name = "position"
    
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'upper_organization', 'manager_name')
    list_filter = ('level', 'upper_organization', 'name')
    search_fields = ['name', 'email', 'manager_name']
    list_editable = ['name', 'address', 'email', 'upper_organization', 'manager_name']    
    inlines = [UserProfileInline,]
    list_per_page = 20
    
            
admin.site.register(Organization, OrganizationAdmin)

admin.site.register(Position)



#admin.site.register(School)
#admin.site.register(SchoolYear)
#admin.site.register(Semester)