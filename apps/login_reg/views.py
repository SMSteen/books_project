from django.shortcuts import render, redirect
from django.contrib import messages
from ..users.models import User

# Create your views here.
def index(request):
    print('login_reg index method, rendering index.html')
    return render(request, 'login_reg/index.html')

def register(request):
    print('login_reg register method, adding new user to db')
    errors = User.objects.registration_valid(request.POST)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags = category)
        return redirect('/')
    else:
        user = User.objects.create_user(request.POST)
        request.session['user_id'] = user.id
        request.session['name'] = user.first_name
        return redirect('/books')

def login(request):
    print('login_reg login method, logging user in')
    errors = User.objects.login_valid(request.POST)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags = category)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['name'] = user.first_name
        return redirect('/books')

def logout(request):
    print('login_reg login method, logging user out')
    #clear all session information
    request.session.flush()
    return redirect('/')