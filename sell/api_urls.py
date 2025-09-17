from django.urls import path
from . import views

urlpatterns = [
    path('brands/', views.get_brands, name='get_brands'),
    path('models/<int:brand_id>/', views.get_models, name='get_models'),
    path('variants/<int:model_id>/', views.get_variants, name='get_variants'),
    path('sell-image/', views.get_background_image, name='get_background_image'),
    path('get-price/', views.get_price, name='get_price'),


    path('how-it-works/', views.how_it_works_data, name='how_it_works'),


]
