from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.messages import get_messages

from .forms import CreateUserForm, CakeForm, OrderForm, CommentForm, LoginForm
from django.contrib import messages
from django.db import transaction
from .models import Cake, Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@transaction.atomic
def register(request):

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('cakesite:private_office')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('cakesite:login')


@transaction.atomic
@login_required
def create_cake_order_view(request):
    if request.method == 'POST':
        cake_form = CakeForm(request.POST)
        order_form = OrderForm(request.POST)
        if order_form.is_valid() and cake_form.is_valid():
            cd_cake = cake_form.cleaned_data
            cd_order = order_form.cleaned_data
            order = Order.objects.create(address=cd_order['address'],
                                         deliver_to=cd_order['deliver_to'],
                                         user=request.user,
                                         )
            cake = Cake.objects.create(levels_count=cd_cake['levels_count'],
                                       cake_form=cd_cake['cake_form'],
                                       topping=cd_cake['topping'],
                                       berries=cd_cake['berries'],
                                       decor=cd_cake['decor'],
                                       inscription=cd_cake['inscription'],
                                       promocode=cd_cake['promocode'],
                                       order=order,
                                       )
            cost = get_order_cost(order.id)
            order.cost = cost
            order.save()
            return redirect('cakesite:confirm_order', order_id=order.id)
    else:
        cake_form = CakeForm()
        order_form = OrderForm(initial={'address': request.user.address})
        return render(request, "create_order.html", {'cake_form': cake_form,
                                                     'order_form': order_form})


@login_required
def get_private_office(request):
    orders = Order.objects.all()
    return render(request, "private_office.html", {'orders': orders})


@login_required
def cancel_order(request, order_id):
    Order.objects.get(id=order_id).delete()
    return render(request, "order_cancellation.html")


@login_required
def confirm_order_view(request, order_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            storage = messages.get_messages(request)
            print(storage)
            cd_comment = comment_form.cleaned_data
            order = Order.objects.get(id=order_id)
            order.comment = cd_comment['comment']
            order.save()
            return redirect('cakesite:confirm_order_done', order_id=order_id)
    else:
        comment_form = CommentForm()
        order = Order.objects.get(id=order_id)
        cake = Cake.objects.get(order=order)
        return render(request,
                      "confirm_order.html",
                      {'comment_form': comment_form,
                       'order': order,
                       'cake': cake})


@login_required
def confirm_order_done(request, order_id):
    return render(request, 'confirm_order_done.html')


def get_order_cost(order_id):
    cost = 0

    order = Order.objects.get(id=order_id)
    cake = Cake.objects.get(order=order)

    if cake.levels_count == '1':
        cost = cost + 400
    if cake.levels_count == '2':
        cost = cost + 750
    if cake.levels_count == '3':
        cost = cost + 1100

    if cake.cake_form == "Квадрат":
        cost = cost + 600
    if cake.cake_form == "Круг":
        cost = cost + 400
    if cake.cake_form == "Прямоугольник":
        cost = cost + 1000

    for topping in cake.topping:
        if topping == "Без топпинга":
            cost = cost
        if topping == "Белый соус":
            cost = cost + 200
        if topping == "Карамельный сироп":
            cost = cost + 180
        if topping == "Кленовый сироп":
            cost = cost + 200
        if topping == "Клубничный сироп":
            cost = cost + 300
        if topping == "Черничный сироп":
            cost = cost + 350
        if topping == "Молочный шоколад":
            cost = cost + 200

    for berry in cake.berries:
        if berry == "Ежевика":
            cost = cost + 400
        if berry == "Малина":
            cost = cost + 300
        if berry == "Голубика":
            cost = cost + 450
        if berry == "Клубника":
            cost = cost + 500

    for decor in cake.decor:
        if decor == "Фисташки":
            cost = cost + 300
        if decor == "Безе":
            cost = cost + 400
        if decor == "Фундук":
            cost = cost + 350
        if decor == "Пекан":
            cost = cost + 300
        if decor == "Маршмеллоу":
            cost = cost + 200
        if decor == "Марципан":
            cost = cost + 280

    if cake.promocode == "ТОРТ":
        cost = cost*0.8

    if cake.inscription:
        cost = cost +500

    if order.deliver_to <= timezone.now() + timedelta(days=1):
        cost = cost * 1.2

    return cost
