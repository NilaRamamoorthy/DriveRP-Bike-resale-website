from django.shortcuts import render
from django.urls import reverse, NoReverseMatch
from .models import HomeContent, BikeCarouselImage, RiderSection, SupportFeature, FAQ, AboutSection, TrustedRidersSection
from django.shortcuts import render, redirect
from .forms import CustomerReviewForm
from .models import CustomerReview
# Helper to safely reverse URL or return raw path if it's not a view name
def safe_reverse(link):
    if not link:
        return "#"
    try:
        return reverse(link)  # Tries to reverse Django view name
    except NoReverseMatch:
        return link if link.startswith('/') else "#"

# Home page view
def home_view(request):
    content = HomeContent.objects.first()
    images = BikeCarouselImage.objects.all()
    rider_section = RiderSection.objects.first()
    support_features = SupportFeature.objects.all().order_by('order')
    faqs = FAQ.objects.all()
    section = TrustedRidersSection.objects.filter(active=True).last()
    content_url = safe_reverse(content.button_link) if content else "#"
    rider_url = safe_reverse(rider_section.button_link) if rider_section else "#"
 # Handle review form submission
    if request.method == 'POST':
        form = CustomerReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Ensure your home URL is named 'home'
    else:
        form = CustomerReviewForm()

    # Reviews (only showing 3 latest as in the design)
    reviews = CustomerReview.objects.order_by('-created_at')[:3]
    context = {
        'content': content,
        'carousel_images': images,
        'rider': rider_section,
        'content_button_url': content_url,
        'rider_button_url': rider_url,
        'support_features': support_features, 
        'faqs': faqs,  
        'trusted_riders_section': section,
        'form': form,  # ✅ Required for review modal
        'reviews': reviews,  # ✅ Review list

        
    }

    return render(request, 'core/home.html', context)

# from django.shortcuts import render, redirect
# from .models import CustomerReview
# from .forms import CustomerReviewForm

# def reviews_view(request):
#     if request.method == 'POST':
#         form = CustomerReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Make sure this URL name matches
#     else:
#         form = CustomerReviewForm()

#     reviews = CustomerReview.objects.order_by('-created_at')[:3]
#     return render(request, 'home.html', {'reviews': reviews, 'form': form})

# About page view

from .models import ApproachSectionImage

def about(request):
    about_section = AboutSection.objects.first()
    approach_images = ApproachSectionImage.objects.all().order_by('order')[:4]

    return render(request, 'core/about.html', {
        'about_section': about_section,
        'approach_images': approach_images,
    })


