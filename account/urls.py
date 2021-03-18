from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name='account'
urlpatterns = [
    path('login/',views.LoginView, name='login'),
    path('logout/',views.LogoutView, name='logout'),
    path('signup/',views.SignupView, name='signup'),

]