from django.contrib import admin
from public.models import RealEstate, Region, City, RealEstateImage, Report

admin.site.register(RealEstate)
admin.site.register(RealEstateImage)
admin.site.register(Region)
admin.site.register(City)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')
