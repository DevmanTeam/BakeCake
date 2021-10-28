from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "cakesite"

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('create_order/', views.create_cake_order_view, name='create_order'),
    path('confirm_order/', views.confirm_order_view, name='confirm_order'),
]
