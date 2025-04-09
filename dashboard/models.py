from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class CustomUser(AbstractUser):
    USER = (
        ('1','Superadmin'),
        ('2','Client'),
        
    )
   

    user_type = models.CharField(choices=USER,max_length=50,default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    
    
class Staff(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address= models.TextField()
    gender=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.admin.username
    