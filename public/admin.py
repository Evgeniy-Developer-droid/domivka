from django.contrib import admin
from public.models import RealEstate, Region, City, RealEstateImage, Report, SEO

# admin.site.register(RealEstate)
admin.site.register(RealEstateImage)
admin.site.register(Region)
admin.site.register(City)


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('region', 'city', 'rooms', 'price', 'type_real_estate','service_type', 'timestamp',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ('keywords', 'description',)

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and SEO.objects.exists():
            retVal = False
        return retVal
