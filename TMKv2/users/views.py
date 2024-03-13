from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('leagues')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('leagues')
        
        else:
            messages.error(request, 'username or password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = UserCreationForm

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account Created!')

            login(request, user)
            return redirect('leagues')
        
        else:
            messages.error(request, 'Error Registering')
        
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)