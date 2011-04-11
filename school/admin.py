from django.contrib import admin
from school.models import School, Class, Teacher, Pupil, Mark, Subject, Term

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'Mark_1'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

admin.site.register(School, MultiDBModelAdmin)
admin.site.register(Class, MultiDBModelAdmin)
admin.site.register(Teacher, MultiDBModelAdmin)
admin.site.register(Pupil, MultiDBModelAdmin)
admin.site.register(Mark, MultiDBModelAdmin)
admin.site.register(Subject, MultiDBModelAdmin)
admin.site.register(Term, MultiDBModelAdmin)

