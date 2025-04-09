"""
URL configuration for commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .import views, superadmin_views,staffviews

urlpatterns = [
    path('', views.LOGIN, name='login'),
    path('dologin',views.dologin, name='dologin'),
    path('dogout',views.dologout, name='logout'),
    path('superadmin/home',superadmin_views.HOME, name = "home"),
    path('profile',views.PROFILE, name = "profile"),
    path('superadmin/staff/add', superadmin_views.ADD_STAFF, name ="add_staff"),
    
    path('Staff/home',staffviews.home,name = "staff_home"),
    path('Staff/updateinformation',staffviews.ADD_INFO,name = "updateinformation"),
    path('Staff/addproducts',staffviews.ADD_PRODUCTS,name = "addproducts"),
    path('Staff/addpeti',staffviews.ADD_PETI,name = "addpeti"),
    path('Staff/viewproducts',staffviews.VIEWPRODUCTS,name = "viewproducts"),
    path('edit-product-name/<int:product_id>/', staffviews.edit_product_name, name='edit_product_name'),
    path('edit-price/<int:product_id>/', staffviews.edit_price, name='edit_price'),
    path('Staff/viewpeti',staffviews.VIEWPETI,name = "viewpeti"),
    path('edit-peti-name/<int:product_id>/', staffviews.edit_peti_name, name='edit_peti_name'),
    path('edit-peti-price/<int:product_id>/', staffviews.edit_peti_price, name='edit_peti_price'),
    path('change_status', staffviews.ajax_change_status, name='ajax_change_status'),
]
