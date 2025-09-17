# from django.urls import path
# from . import views

# app_name = 'sell'

# urlpatterns = [
#     path('', views.sell_home, name='sell_bike'),
   

#     # path('submit/', views.sell_bike_page, name='sell_bike_page'),
    
#     path("submit/", views.sell_bike_page, name="sell_bike_page_no_price"),

#     path('submit/<int:estimated_price>/', views.sell_bike_page, name='sell_bike_page'),

    
#     path('api/brands/', views.get_brands, name='get_brands'),
#     path('api/models/<int:brand_id>/', views.get_models, name='get_models'),
#     path('api/variants/<int:model_id>/', views.get_variants, name='get_variants'),
#     path('api/sell-image/', views.get_background_image, name='get_background_image'),
# ]

from django.urls import path
from . import views

app_name = 'sell'

urlpatterns = [
    path('', views.sell_home, name='sell_bike'),
    path('submit/', views.sell_bike_page, name='sell_bike_page'),

    path('api/v1/get-price/', views.get_price, name='get_price_api'),
    path('api/brands/', views.get_brands, name='get_brands_api'),
    path('api/models/<int:brand_id>/', views.get_models, name='get_models_api'),
    path('api/variants/<int:model_id>/', views.get_variants, name='get_variants_api'),
    path('api/sell-image/', views.get_background_image, name='get_background_image_api'),
    path('api/how-it-works/', views.how_it_works_data, name='how_it_works_api'),
]

