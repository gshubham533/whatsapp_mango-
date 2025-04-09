from itertools import product
from unicodedata import name
from django.db import models
from dashboard.models import CustomUser,Staff





class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    catalog_id = models.CharField(max_length=100,blank=True)
    curr = models.CharField(max_length=100,blank=True)
    item_price = models.CharField(max_length=100,blank=True)
    product_id = models.CharField(max_length=100,blank=True)
    quantity = models.CharField(max_length=100,blank=True)
    wa_id = models.CharField(max_length=18,blank=False)
    msg_id = models.CharField(max_length=110,unique=True)
    msg = models.TextField(default="")
    interactive_id = models.CharField(max_length=150,default="")
    interactive_desc = models.CharField(max_length=150,default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    msg_type = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    mime_type = models.CharField(max_length=30,default="")
    media_id = models.CharField(max_length=60,default="")
    img_path = models.CharField(max_length=60,default="") 
    
    
# class Products(models.Model):
#     order_id = models.ForeignKey(Messages, null=True, on_delete=models.CASCADE)
#     id = models.AutoField(primary_key=True)
#     product_idd = models.CharField(max_length=100,blank=True)
#     product_quantity = models.CharField(max_length=100,blank=True)
#     catalog_idd = models.CharField(max_length=100,blank=True)
#     currency = models.CharField(max_length=10,blank=True)
#     item_pricee = models.CharField(max_length=100,blank=True)


# class MasterProducts(models.Model):
#     product_id = models.CharField(max_length=100,blank=True)
#     product_name = models.CharField(max_length=100,blank=True)
#     price = models.CharField(max_length=100,blank=True)


# class finalordertable(models.Model):
#     wa_id = models.CharField(blank=False,unique=True,max_length=17)
#     wa_name = models.CharField(max_length=100,blank=True)
#     Address = models.CharField(max_length=100,blank=True)
#     pincode = models.CharField(max_length=8,blank=True)
#     Tracking_url = models.CharField(max_length=100,blank=True)


# class OrderedProducts(models.Model):
#     order_id = models.ForeignKey(finalordertable, null=True, on_delete=models.CASCADE)
#     id = models.AutoField(primary_key=True)
#     product_idd = models.CharField(max_length=100,blank=True)
#     product_quantity = models.CharField(max_length=100,blank=True)
#     catalog_idd = models.CharField(max_length=100,blank=True)
#     currency = models.CharField(max_length=10,blank=True)
#     item_pricee = models.CharField(max_length=100,blank=True)


class Sellers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="seller_admin_id", null=True, blank=True) 
    seller_name = models.CharField(max_length=100,blank=True)
    seller_phone = models.CharField(max_length=100,blank=True)
    cod_status = models.BooleanField(default=True)
    qr_code = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True) 


class Contacts(models.Model):
    id = models.AutoField(primary_key=True)
    flow = models.CharField(max_length=100,blank=True)
    wa_id = models.CharField(blank=False,unique=True,max_length=17)
    wa_name = models.CharField(max_length=100,blank=True)
    pincode = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100,blank=True)
    cust_lead = models.ForeignKey(Sellers, on_delete=models.CASCADE, null=True, blank=True)
    peti_id = models.CharField(max_length=100,blank=True)
    quantity = models.CharField(max_length=100,blank=True)
    payment_option = models.CharField(max_length=100,blank=True)
    ordered_product_id = models.CharField(max_length=100,blank=True,default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Sellers,on_delete=models.CASCADE, related_name="product_seller_id",null=True, blank=True)
    product_name = models.CharField(max_length=100,blank=True)
    price = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 



class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True)
    phone = models.CharField(blank=False,max_length=17)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE,default=1)
    quantity = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=100,blank=True)
    comments = models.CharField(max_length=100,blank=True)
    payment_option = models.CharField(max_length=100,blank=True)
    payment_status = models.BooleanField(max_length=100,blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    dispatch =models.BooleanField(default=False)


class Peti(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Sellers,on_delete=models.CASCADE,default=1)
    price = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


