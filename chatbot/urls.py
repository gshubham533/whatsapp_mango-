from django import urls
from django.contrib import admin
from django.urls import URLPattern, path
from chatbot import views


urlpatterns = [
        path('webhook',views.webhook,name="webhook" ),
                                                                  #Request will be send to webhook function in views.py    
]