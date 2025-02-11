from django.contrib import admin
from .models import Category,Customer,Product,Profile,Order
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)



# Mix Profile Info and User Info
class ProfileInline(admin.StackedInline):
    model=Profile 
    

# Extend User Model    
class UserAdmin(admin.ModelAdmin):
    model=User
    field=['username','first_name','last_name', 'email']
    inlines=[ProfileInline]
    
admin.site.unregister(User)   
admin.site.register(User,UserAdmin) 
    
