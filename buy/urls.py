from django.urls import path
from . import views

app_name = 'buy'

urlpatterns = [
    path('', views.bike_list, name='buy_bike'), 
    path('<int:pk>/', views.bike_detail, name='bike_detail'),
    path('payment/<int:bike_id>/', views.payment_view, name='payment'),

    # add more buy-related URLs here
]
