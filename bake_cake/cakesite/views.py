from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CakeForm, OrderForm, CommentForm
from django.contrib import messages
from django.db import transaction
from .models import Cake, Order
from django.contrib.auth.decorators import login_required

# Create your views here.
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, username)
            redirect('')
        messages.info(request, 'user name is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)    


def logoutUser(request):
    logout(request)
    return redirect('login')


@transaction.atomic
@login_required
def create_cake_order_view(request):
    if request.method == 'POST':
        cake_form = CakeForm(request.POST)
        order_form = OrderForm(request.POST)
        if order_form.is_valid() and cake_form.is_valid():
            cd_cake = cake_form.cleaned_data
            cd_order = order_form.cleaned_data
            print(cd_cake)
            print(cd_order)
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
            return redirect('cakesite:confirm_order', order_id=order.id)
    else:
        cake_form = CakeForm()
        order_form = OrderForm()
        return render(request, "create_order.html", {'cake_form': cake_form,
                                                     'order_form': order_form})


@login_required
def confirm_order_view(request, order_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cd_comment = comment_form.cleaned_data
            order = Order.objects.get(id=order_id)
            order.comment = cd_comment['comment']
            order.save()
            return redirect('cakesite:confirm_order_done', order_id=order_id)
    else:
        comment_form = CommentForm()
        return render(request, "confirm_order.html", {'comment_form': comment_form})


@login_required
def confirm_order_done(request, order_id):
    return render(request, 'confirm_order_done.html')


def get_order_cost(order_id):
    pass