from django.shortcuts import render
from django.shortcuts import render,redirect, HttpResponse
from dashboard.EmailBackend import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dashboard.models import CustomUser



# Create your views here.
def LOGIN(request):
    return render(request,'login.html')

def dologin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return HttpResponse('This is student')
            else:
                messages.error(request,'Email and Password are invalid')
                return redirect('login')
        else:
            messages.error(request,'Email and Password are invalid')
            return redirect('login')
    
def dologout(request):
    logout(request)
    return redirect("login")

def PROFILE(request):
    user = CustomUser.objects.get(id= request.user.id)
    
    
    
    context = {
        'user': user,

    }
    return render(request,'profile.html',context)