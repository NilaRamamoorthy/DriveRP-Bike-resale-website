from django.core.paginator import Paginator
from django.db.models import Min, Max
from django.shortcuts import render
from .models import BikeListing
from django.db import models
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404, redirect
from buy.models import BikeListing

# def buy_home(request):
#     return render(request, 'buy/bike.html')


def bike_list(request):
    # Base queryset first
    bikes = BikeListing.objects.all()

    print("Bikes count:", bikes.count())  # Debug after defining queryset

    # Get distinct values
    brands = BikeListing.objects.values_list('brand', flat=True).distinct().order_by('brand')
    fuel_types = BikeListing.objects.values_list('fuel_type', flat=True).distinct().order_by('fuel_type')
    years = BikeListing.objects.values_list('year', flat=True).distinct().order_by('year')
    colors = BikeListing.objects.values_list('color', flat=True).distinct().order_by('color')
    engine_ccs = BikeListing.objects.values_list('engine_cc', flat=True).distinct().order_by('engine_cc')
    price_range = BikeListing.objects.aggregate(min_price=Min('price'), max_price=Max('price'))

    # GET filter inputs
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    selected_brands = request.GET.getlist('brand')
    selected_categories = request.GET.getlist('category')


    selected_fuel_types = request.GET.getlist('fuel_type')
    min_year = BikeListing.objects.aggregate(min_year=models.Min('year'))['min_year']
    max_year = min(datetime.datetime.now().year, BikeListing.objects.aggregate(max_year=models.Max('year'))['max_year'])
    selected_min_year = request.GET.get('min_year')
    selected_max_year = request.GET.get('max_year')
    selected_km = request.GET.get('km')


    selected_colors = request.GET.getlist('color')
    # selected_engine_ccs = request.GET.getlist('engine_cc')
    selected_engine_trim = request.GET.get('engine_trim')

    sort_option = request.GET.get('sort', 'newest')

    # Apply filters
    if min_price:
        bikes = bikes.filter(price__gte=min_price)
    if max_price:
        bikes = bikes.filter(price__lte=max_price)
    if selected_brands:
        bikes = bikes.filter(brand__in=selected_brands)
    if selected_categories:
        bikes = bikes.filter(category__in=selected_categories)
    if selected_fuel_types:
        bikes = bikes.filter(fuel_type__in=selected_fuel_types)
    if min_year:
        bikes = bikes.filter(year__gte=min_year)
    if max_year:
        bikes = bikes.filter(year__lte=max_year)
    
    if selected_min_year:
        bikes = bikes.filter(year__gte=selected_min_year)
    if selected_max_year:
        bikes = bikes.filter(year__lte=selected_max_year)
    if selected_colors:
        bikes = bikes.filter(color__in=selected_colors)
    if selected_engine_trim:
        bikes = bikes.filter(engine_cc__lt=selected_engine_trim)

    if selected_km:
        bikes = bikes.filter(kilometers_driven__lte=selected_km)
    # Sorting
    if sort_option == 'price_low_high':
        bikes = bikes.order_by('price')
    elif sort_option == 'price_high_low':
        bikes = bikes.order_by('-price')
    elif sort_option == 'km_low_high':
        bikes = bikes.order_by('kilometers_driven')
    elif sort_option == 'km_high_low':
        bikes = bikes.order_by('-kilometers_driven')
    elif sort_option == 'year_old_new':
        bikes = bikes.order_by('year')
    elif sort_option == 'year_new_old':
        bikes = bikes.order_by('-year')
    else:
        bikes = bikes.order_by('-created_at')

    # Pagination
    paginator = Paginator(bikes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_bikes': bikes.count(),
        'price_range': price_range,
        'brands': brands,
        'selected_categories': selected_categories,
        'fuel_types': fuel_types,
        'years': years,
        'colors': colors,
        'engine_ccs': engine_ccs,
        'selected_brands': selected_brands,
        'selected_fuel_types': selected_fuel_types,
        'min_year': min_year,
        'max_year': max_year,
        'selected_min_year': selected_min_year or min_year,
        'selected_max_year': selected_max_year or max_year,
        'year_range': BikeListing.objects.aggregate(min_year=models.Min('year'), max_year=models.Max('year')),
        'selected_km': selected_km,
        'selected_colors': selected_colors,
        'selected_engine_trim': selected_engine_trim,

        'min_price': min_price or price_range['min_price'],
        'max_price': max_price or price_range['max_price'],
        'sort_option': sort_option,
    }

    return render(request, 'buy/bike.html', context)


# Bike details
from django.shortcuts import render, get_object_or_404
from .models import BookingStep

def bike_detail(request, pk):
    bike = get_object_or_404(BikeListing, pk=pk)
    steps = BookingStep.objects.all()  # <-- include this here!
    return render(request, 'buy/bike_details.html', {
        'bike': bike,
        'steps': steps,
    })




@login_required(login_url='login')  # Redirects to login if not logged in
def payment_view(request, bike_id):
    bike = get_object_or_404(BikeListing, pk=bike_id)

    if bike.booked:
        return redirect('buy:bike_detail', pk=bike_id)

    if request.method == "POST":
        bike.booked = True
        bike.save()
        return redirect('buy:bike_detail', pk=bike_id)

    return render(request, 'buy/payment.html', {
        'bike': bike,
        'base_price': bike.price,  # ✅ Pass price explicitly
    })

