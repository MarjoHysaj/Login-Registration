from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, "index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        return redirect('/success')

def login(request):
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request,value)
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)
