from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import Cake, Order


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CakeForm(forms.ModelForm):
    TOPPING_CHOICES = [
        ("Без топпинга", "без топпинга"),
        ("Белый соус", "белый соус"),
        ("Карамельный сироп", "карамельный сироп"),
        ("Кленовый сироп", "кленовый сироп"),
        ("Клубничный сироп", "клубничный сироп"),
        ("Черничный сироп", "черничный сироп"),
        ("Молочный шоколад", "молочный шоколад"),
    ]
    BERRIES_CHOICES = [
        ("Ежевика", "ежевика"),
        ("Малина", "малина"),
        ("Голубика", "голубика"),
        ("Клубника", "клубника"),
    ]

    DECOR_CHOICES = [
        ("Фисташки", "фисташки"),
        ("Безе", "безе"),
        ("Фундук", "фундук"),
        ("Пекан", "пекан"),
        ("Маршмеллоу", "маршмеллоу"),
        ("Марципан", "марципан"),
    ]

    class Meta:
        model = Cake
        fields = ('levels_count', 'cake_form', 'topping', 'berries',
                  'decor', 'inscription', 'promocode')


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('address', 'deliver_to')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('comment',)