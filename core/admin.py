from django.contrib import admin
from .models import SiteSettings, LoginImage
from .models import HomeContent, BikeCarouselImage, RiderSection, SupportFeature, FAQ, AboutSection, TrustedRidersSection, CustomerReview
from .models import ApproachSectionImage
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'logo', 'footer_logo','footer_bike')  # ✅ Include your new field

admin.site.register(LoginImage)


# Home
admin.site.register(HomeContent)
admin.site.register(BikeCarouselImage)
admin.site.register(RiderSection)
admin.site.register(TrustedRidersSection)
admin.site.register(CustomerReview)

@admin.register(SupportFeature)
class SupportFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)
admin.site.register(FAQ)


# About
admin.site.register(AboutSection)


admin.site.register(ApproachSectionImage)
