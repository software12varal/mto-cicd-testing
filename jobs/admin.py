from django.contrib import admin

from jobs.models import MTOAdminUser, AdminRoles,  MicroTask, MTOJob, EvaluationStatus, Jobs, PaymentStatus, Jobstatus


class MTOJobCategoryAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'varal_job_posting_db'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class MTORolesAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'varal_job_posting_db'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(EvaluationStatus)
admin.site.register(MTOAdminUser)
admin.site.register(MTOJob)
# admin.site.register(MTOJobCategory, MTOJobCategoryAdmin)
admin.site.register(AdminRoles, MTORolesAdmin)
admin.site.register(MicroTask)
# admin.site.register(MALRequirement),
admin.site.register(Jobs),
admin.site.register(PaymentStatus),
admin.site.register(Jobstatus)
