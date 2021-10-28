from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CakeForm
from django.contrib import messages

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


def make_cake_view(request):

    if request.method == 'GET':
        cake_form = CakeForm()
        return render(request, "make_cake.html", {'cake_form': cake_form})
