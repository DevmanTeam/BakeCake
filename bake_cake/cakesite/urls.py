from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "cakesite"

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('add_cake/', views.make_cake_view, name='add_cake'),
]
