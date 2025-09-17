from django.shortcuts import render, redirect
from .models import SellHero
from django.http import JsonResponse
from .models import Brand, Model as BikeModel, Variant, SellImage
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import HowItWorksStep
from .forms import BikeListingForm, BikeImageForm
from buy.models import BikeImage
from django.urls import reverse
import random
from buy.models import Brand, Model, Variant




def sell_home(request):
    hero = SellHero.objects.filter(active=True).last()
    return render(request, 'sell/sell.html', {'hero': hero})


def get_brands(request):
    brands = list(Brand.objects.values('id', 'name'))
    return JsonResponse({'brands': brands})

def get_models(request, brand_id):
    models = list(BikeModel.objects.filter(brand_id=brand_id).values('id', 'name'))
    return JsonResponse({'models': models})

def get_variants(request, model_id):
    variants = list(Variant.objects.filter(model_id=model_id).values('id', 'name', 'launch_year'))
    return JsonResponse({'variants': variants})

def get_background_image(request):
    image = SellImage.objects.filter(active=True).last()
    image_url = image.image.url if image else ''
    return JsonResponse({'image_url': image_url})



@csrf_exempt
def get_price(request):
    import sys
    print("HIT get_price endpoint", file=sys.stderr)

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            brand_id = int(data.get("brand_id"))
            model_id = int(data.get("model_id"))
            variant_id = int(data.get("variant_id"))
            year = int(data.get("year"))
            kms = data.get("kms")
            owner = data.get("owner")

            # 💡 Basic price logic
            base_price = 100000
            age = 2025 - year
            depreciation = base_price * (0.1 * age)

            if owner == "2nd":
                depreciation += 5000
            elif owner == "3rd":
                depreciation += 10000

            if "20,001+" in kms:
                depreciation += 15000
            elif "10,001-20,000" in kms:
                depreciation += 10000
            elif "5,001-10,000" in kms:
                depreciation += 5000

            final_price = max(base_price - depreciation, 20000)

            # ✅ Save to session
            request.session['sell_data'] = {
                'brand': brand_id,
                'model': model_id,
                'variant': variant_id,
                'year': year,
                'kms_driven': kms,
                'owner': owner,
                'price': int(final_price),
            }

            return JsonResponse({"price": int(final_price)})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)




def how_it_works_data(request):
    steps = HowItWorksStep.objects.all()
    data = []

    for step in steps:
        data.append({
            'title': step.title,
            'image': request.build_absolute_uri(step.image.url) if step.image else ''
        })

    return JsonResponse({'steps': data})





def sell_bike_page(request):
    sell_data = request.session.get('sell_data')
    if not sell_data:
        return redirect('sell:sell_bike')

    manual_fields = ['brand', 'model', 'variant', 'year', 'kilometers_driven', 'owner']

    if request.method == 'POST':
        # ✅ Make a mutable copy of POST and clean kilometers_driven
        post_data = request.POST.copy()
        print("RAW POST:", request.POST)
        if 'kilometers_driven' in post_data:
            raw_kms = str(post_data['kilometers_driven'])
            cleaned_kms = ''.join(ch for ch in raw_kms if ch.isdigit())  # keep only digits
            post_data['kilometers_driven'] = cleaned_kms or '0'
            print("CLEANED KMS:", post_data['kilometers_driven'])
        listing_form = BikeListingForm(post_data, request.FILES)
        image_form = BikeImageForm()

        if listing_form.is_valid():
            images = request.FILES.getlist('image')

            if not images:
                listing_form.add_error(None, "Please upload at least one image.")
                remaining_form = BikeListingForm()
                for field_name in manual_fields:
                    if field_name in remaining_form.fields:
                        remaining_form.fields.pop(field_name)

                return render(request, 'sell/sell_form.html', {
                    'listing_form': listing_form,
                    'remaining_form': remaining_form,
                    'image_form': image_form,
                    'estimated_price': sell_data.get('price'),
                    'lock_fields': True,
                })

            # ✅ Save bike
            bike = listing_form.save(commit=False)
            bike.price = sell_data.get('price', 0)
            bike.save()

            for img in images:
                BikeImage.objects.create(bike=bike, image=img)

            # Set first image as main
            first_img = bike.gallery_images.first()
            if first_img:
                bike.image = first_img.image
                bike.save()

            if 'sell_data' in request.session:
                del request.session['sell_data']

            # Prepare fresh forms
            remaining_form = BikeListingForm()
            for field_name in manual_fields:
                if field_name in remaining_form.fields:
                    remaining_form.fields.pop(field_name)

            return render(request, 'sell/sell_form.html', {
                'listing_form': BikeListingForm(),
                'remaining_form': remaining_form,
                'image_form': BikeImageForm(),
                'show_modal': True,
                'bike_id': bike.id,
                'estimated_price': bike.price,
                'lock_fields': True,
            })
        else:
            # ❌ Debug invalid form
            print("FORM ERRORS:", listing_form.errors)

            remaining_form = BikeListingForm()
            for field_name in manual_fields:
                if field_name in remaining_form.fields:
                    remaining_form.fields.pop(field_name)

            return render(request, 'sell/sell_form.html', {
                'listing_form': listing_form,
                'remaining_form': remaining_form,
                'image_form': image_form,
                'estimated_price': sell_data.get('price'),
                'lock_fields': True,
            })

    else:  # GET request
        # ✅ Clean kms_driven before setting as initial
        kms_value = str(sell_data.get('kms_driven', '')).replace(',', '').strip()

        initial_data = {
            'brand': sell_data.get('brand'),
            'model': sell_data.get('model'),
            'variant': sell_data.get('variant'),
            'year': sell_data.get('year'),
            'kilometers_driven': kms_value,
            'owner': sell_data.get('owner'),
        }
        listing_form = BikeListingForm(initial=initial_data)
        image_form = BikeImageForm()

        # Fetch human-readable names
        try:
            brand_name = Brand.objects.get(id=sell_data.get('brand')).name
        except Brand.DoesNotExist:
            brand_name = "Unknown Brand"

        try:
            model_name = Model.objects.get(id=sell_data.get('model')).name
        except Model.DoesNotExist:
            model_name = "Unknown Model"

        try:
            variant_name = Variant.objects.get(id=sell_data.get('variant')).name
        except Variant.DoesNotExist:
            variant_name = "Unknown Variant"

        remaining_form = BikeListingForm()
        for field_name in manual_fields:
            if field_name in remaining_form.fields:
                remaining_form.fields.pop(field_name)

        return render(request, 'sell/sell_form.html', {
            'listing_form': listing_form,
            'remaining_form': remaining_form,
            'image_form': image_form,
            'estimated_price': sell_data.get('price'),
            'lock_fields': True,
            'brand_name': brand_name,
            'model_name': model_name,
            'variant_name': variant_name,
        })


from django import forms

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if self.attrs is None:
            self.attrs = {}
        self.attrs['multiple'] = True



from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    try:
        return field.as_widget(attrs={"class": css_class})
    except AttributeError:
        return field  # Return the field as-is if it's not a form field

