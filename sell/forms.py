# from django import forms
# from buy.models import BikeListing, BikeImage


# # Custom widget to allow multiple uploads
# class MultiFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True

#     def __init__(self, attrs=None):
#         default_attrs = {'multiple': 'multiple'}
#         if attrs:
#             default_attrs.update(attrs)
#         super().__init__(attrs=default_attrs)





# class BikeListingForm(forms.ModelForm):
#     class Meta:
#         model = BikeListing
#         fields = [
#             'brand', 'model', 'variant', 'year', 'engine_cc', 'fuel_type',
#             'kilometers_driven', 'owner', 'location', 'color',
#             'registration_year', 'rc_available', 'finance', 'insurance',
#             'warranty', 'transmission', 'refurbished', 'rto_state', 'rto_city',
#             'category'
#         ]
#     def __init__(self, *args, **kwargs):
#         estimated_price = kwargs.pop("estimated_price", None)  # take extra arg from view
#         super().__init__(*args, **kwargs)

       

# class BikeImageForm(forms.ModelForm):
#     image = forms.ImageField(widget=MultiFileInput)

#     class Meta:
#         model = BikeImage
#         fields = ['image']
from django import forms
from buy.models import BikeListing, BikeImage
from sell.models import Brand, Model, Variant
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    def __init__(self, attrs=None):
        final_attrs = {'multiple': 'multiple'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

class BikeListingForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label="Select Brand")
    model = forms.ModelChoiceField(queryset=Model.objects.all(), empty_label="Select Model")
    variant = forms.ModelChoiceField(queryset=Variant.objects.all(), empty_label="Select Variant")
    class Meta:
        model = BikeListing
        fields = [
            'brand', 'model', 'variant', 'year', 'engine_cc', 'fuel_type',
            'kilometers_driven', 'owner', 'location', 'color',
            'registration_year', 'rc_available', 'finance', 'insurance',
            'warranty', 'transmission', 'refurbished', 'rto_state', 'rto_city',
            'category'
        ]

class BikeImageForm(forms.ModelForm):
    image = forms.ImageField(widget=MultiFileInput)

    class Meta:
        model = BikeImage
        fields = ['image']
