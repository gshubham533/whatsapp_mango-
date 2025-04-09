from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from dashboard.models import CustomUser, Staff
from django.contrib import messages
from chatbot.models import Sellers

@login_required(login_url='/')
def HOME(request):
    return render(request,'superadmin/home.html')

def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        shopname = request.POST.get("shopname")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        
        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request,"Email is already taken")
            return redirect("add_staff")                
        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request,"Username is already taken")
            return redirect("add_staff")   
        
        else:
            user = CustomUser(first_name = first_name,last_name = last_name,username=username,email = email,profile_pic= profile_pic,user_type = 2)  
            user.set_password(password)
            user.save()
            
            seller = Sellers(admin=user, seller_name=shopname)
            seller.save()
            
            staff = Staff(
                admin = user,
                gender = gender
            )       
            staff.save()
            messages.success(request,"Staff is successfully added")
            return redirect("add_staff")
    return render(request,"superadmin/add_staff.html")