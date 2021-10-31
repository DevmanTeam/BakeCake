from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "cakesite"

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('create_order/', views.create_cake_order_view, name='create_order'),
    path('confirm_order/<int:order_id>/', views.confirm_order_view, name='confirm_order'),
    path('confirm_order/<int:order_id>/done/', views.confirm_order_done, name='confirm_order_done'),
]
