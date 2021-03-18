from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('updatecart/', views.updatecart, name='updatecart'),
    path('cartsummary/', views.cartsummaryview, name='cartsummary'),
    path('checkout/', views.checkoutview, name='checkout'),
    path('tracker/', views.trackorderview, name='tracker'),
    
]