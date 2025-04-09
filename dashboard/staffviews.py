from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import make_password
from chatbot.models import Sellers, Products,Orders,  Peti
from dashboard.models import CustomUser, Staff
from django.contrib import messages
from django.http import JsonResponse
def home(request):
    staff_user = request.user
    staff = Staff.objects.get(admin=staff_user)
    seller = staff.admin.seller_admin_id
    orders = Orders.objects.filter(product_id__seller=seller).select_related('product_id').values('name', 'quantity', 'address', 'payment_status', 'product_id__product_name','id','dispatch','comments')
    count = orders.count()
    context = {'orders': orders, 'count': count}
    return render(request,"staff/staffhome.html",context)

def ADD_INFO(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            shopname = request.POST.get("shopname")
            # password = request.POST.get("password")
            gender = request.POST.get("gender")
            print(request.user)
            print(first_name,last_name,username,shopname,gender)
            staff = Staff.objects.get(admin=request.user)
            print("staff",staff)
            staff.gender = gender
            staff.save()
            
            customuser = CustomUser.objects.get(id=request.user.id)
            print("customuser",customuser)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.username = username
            # customuser.password = make_password(password)
            customuser.save()
            
            seller = Sellers.objects.get(admin=request.user)
            print("seller",seller)
            seller.seller_name = shopname
            seller.save()
            
            messages.success(request, 'Information updated successfully.')
            return redirect('updateinformation')
            
   
    return render(request,'staff/addinfo.html')


def ADD_PRODUCTS(request):
    if request.method == "POST":
        product_name = request.POST.get('Product1')
        price = request.POST.get('Price1')
        user = request.user
        try:
            seller = user.seller_admin_id
            product = Products(seller=seller, product_name=product_name, price=price)
            product.save()
            messages.success(request, "Product added successfully")
            return redirect('addproducts')
        except Sellers.DoesNotExist:
            messages.error(request, "You are not authorized to add products")
            return redirect('addproducts')
    else:
        return render(request, 'staff/addproducts.html')

def ADD_PETI(request):
    if request.method == "POST":
        peti = request.POST.get('Peti')
        description = request.POST.get('description')
        user = request.user
        try:
            seller = user.seller_admin_id
            peti = Peti(seller=seller, name=peti, price=description)
            peti.save()
            messages.success(request, "Product added successfully")
            return redirect('addpeti')
        except Sellers.DoesNotExist:
            messages.error(request, "You are not authorized to add products")
            return redirect('addpeti')
    else:
        return render (request,"staff/addpeti.html")
    
   
def VIEWPRODUCTS(request):
    user = request.user
    # if not user.is_staff:
    #     return HttpResponse("Unauthorized access")
    try:
        seller = user.seller_admin_id
        print(seller)
        products = Products.objects.filter(seller=seller)
        context = {
            'products': products,
        }
        return render(request, 'staff/viewproducts.html', context)
    except Sellers.DoesNotExist:
        return HttpResponse("Seller not found")


def edit_product_name(request, product_id):
    if request.method == 'POST':
        user = request.user
        seller = user.seller_admin_id
        product = Products.objects.get(seller=seller,id=product_id)
        product.product_name = request.POST['product_name']
        product.save()
    return redirect('viewproducts')

def edit_price(request, product_id):
    if request.method == 'POST':
        user = request.user
        seller = user.seller_admin_id
        print(seller)
        product = Products.objects.get(seller=seller,id=product_id)
        product.price = request.POST['price']
        product.save()
    return redirect('viewpeti')

def VIEWPETI(request):
    user = request.user
    # if not user.is_staff:
    #     return HttpResponse("Unauthorized access")
    try:
        seller = user.seller_admin_id
        print(seller)
        products = Peti.objects.filter(seller=seller)
        context = {
            'products': products,
        }
        return render(request, 'staff/viewpeti.html', context)
    except Sellers.DoesNotExist:
        return HttpResponse("Seller not found")
    

def edit_peti_name(request, product_id):
    if request.method == 'POST':
        user = request.user
        seller = user.seller_admin_id
        product = Peti.objects.get(seller=seller,id=product_id)
        product.name = request.POST['product_name']
        product.save()
    return redirect('viewpeti')

def edit_peti_price(request, product_id):
    if request.method == 'POST':
        user = request.user
        seller = user.seller_admin_id
        print(seller)
        product = Peti.objects.get(seller=seller,id=product_id)
        product.price = request.POST['price']
        product.save()
    return redirect('viewpeti')


# def ajax_change_status(request):
#     if request.method == "GET":
        
#         user_id = request.GET.get('user_id', False)
#         # job_id = request.GET.get('job_id', False)
#         # first you get your Job model
#         if user_id:
#             job = Orders.objects.get(pk=user_id)
#             print(job)
#             try:
#                 job.dispatch = True
#                 job.save()
#                 resmessage = job.name + " has checked in. "
#                 return JsonResponse({"success": True,"response":resmessage})
#             except Exception as e:
#                 return JsonResponse({"success": False})
#         else:
#             return JsonResponse({"success": False})
#     else:
#         return HttpResponse("Hiiiiii")  
def ajax_change_status(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id', False)
        if user_id:
            try:
                job = Orders.objects.get(pk=user_id)
                job.dispatch = True
                job.save()
                resmessage = job.name + "'s order got dispatched."
                return JsonResponse({"success": True, "response": resmessage})
            except Orders.DoesNotExist:
                return JsonResponse({"success": False, "response": "Invalid user ID"})
            except Exception as e:
                return JsonResponse({"success": False, "response": str(e)})
        else:
            return JsonResponse({"success": False, "response": "User ID not provided"})
    else:
        return HttpResponse("Hiiiiii")
