from django.contrib import admin
from .models import BikeListing

admin.site.register(BikeListing)
# admin.site.register(BikeImage)


from django.contrib import admin
from .models import BikeListing, BikeImage

# Inline for extra gallery images
class BikeImageInline(admin.TabularInline):  # or use admin.StackedInline
    model = BikeImage
    extra = 1  # How many empty forms to show by default


from .models import BookingStep

@admin.register(BookingStep)
class BookingStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title')
    ordering = ('step_number',)
    search_fields = ('title',)
