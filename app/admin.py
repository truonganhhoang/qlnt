from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from app.models import Organization, UserProfile, Membership
#, SchoolYear, Semester

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'organization', 'position', 'email', 'phone')
    list_editable = ['first_name', 'last_name', 'organization', 'position', 'email', 'phone']
    list_filter = ('organization')
    search_fields = ['first_name', 'last_name', 'organization',  'email', 'phone', 'notes']

class UserProfileInline (admin.StackedInline):
    model = UserProfile
    max_num = 1
    
class CustomizedUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

class MembershipInline (admin.StackedInline):
    model = Membership
    extra = 1
    
class UserAdmin (admin.ModelAdmin):
    inlines = [MembershipInline,]
     
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'upper_organization', 'manager_name')
    list_filter = ('level', 'upper_organization', 'name')
    search_fields = ['name', 'email', 'manager_name']
    list_editable = ['name', 'address', 'email', 'upper_organization', 'manager_name']    
    inlines = [MembershipInline,]
    list_per_page = 20
    
admin.site.register(Organization, OrganizationAdmin)

