from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import Cake


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
#
#
class CakeForm(forms.ModelForm):
    TOPPING_CHOICES = [
        ("Без топпинга", "без топпинга"),
        ("Белый соус", "белый соус"),
        ("Карамельный сироп", "карамельный сироп"),
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

    topping = forms.MultipleChoiceField(choices=TOPPING_CHOICES)
    berries = forms.MultipleChoiceField(choices=BERRIES_CHOICES)
    decor = forms.MultipleChoiceField(choices=DECOR_CHOICES)

    class Meta:
        model = Cake
        fields = ('levels_count', 'cake_form', 'topping', 'berries',
                  'decor', 'inscription', 'promocode')
