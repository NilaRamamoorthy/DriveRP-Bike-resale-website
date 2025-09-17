from django.contrib import admin
from .models import Brand, Model, Variant, SellImage

# Optional: Inline model admin to manage related objects easily
class ModelInline(admin.TabularInline):
    model = Model
    extra = 1

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [ModelInline]  # Allows adding Models directly from Brand page

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand']
    list_filter = ['brand']
    search_fields = ['name']
    inlines = [VariantInline]  # Allows adding Variants directly from Model page

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'model', 'launch_year']
    list_filter = ['model']
    search_fields = ['name']

@admin.register(SellImage)
class SellImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'active']
    list_filter = ['active']


from .models import HowItWorksStep

@admin.register(HowItWorksStep)
class HowItWorksStepAdmin(admin.ModelAdmin):
    list_display = ('order', 'title')
    ordering = ('order',)


from django.contrib import admin
from .models import SellHero

admin.site.register(SellHero)

