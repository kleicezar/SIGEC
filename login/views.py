from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        return render(request, 'login/login.html')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.get(email=email)
    return HttpResponse(username)