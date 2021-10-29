from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Cake, Order


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CakeForm(forms.ModelForm):
    inscription = forms.DateTimeField(label='Надпись',
                                      required=False,
                                      help_text='Мы можем разместить на торте любую надпись, например: «С днем рождения!»')

    class Meta:
        model = Cake
        fields = ('levels_count', 'cake_form', 'topping', 'berries',
                  'decor', 'promocode')


class OrderForm(forms.ModelForm):
    # deliver_to = forms.DateTimeField(label='Время и дата доставки',
    #                                  initial=timezone.now())

    class Meta:
        model = Order
        fields = ('address', 'deliver_to')

    def clean_deliver_to(self):
        deliver_to = self.cleaned_data['deliver_to']

        if deliver_to < timezone.now():
            raise ValidationError('Время доставки не может быть меньше текущего времени')
        return deliver_to


class CommentForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('comment',)