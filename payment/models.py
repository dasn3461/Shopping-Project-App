from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import datetime

# Create your models here.
class ShippingAddress(models.Model):
    DIVISION_CHOICES = (
        ('Dhaka', 'Dhaka'),
        ('Chittagong', 'Chittagong'),
        ('Rajshahi', 'Rajshahi'),
        ('Khulna', 'Khulna'),
        ('Barishal', 'Barishal'),
        ('Sylhet', 'Sylhet'),
        ('Rangpur', 'Rangpur'),
        ('Mymensingh', 'Mymensingh'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.EmailField()
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_division = models.CharField(max_length=255, choices=DIVISION_CHOICES)
    shipping_zipcode = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255, default="Bangladesh")
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"
        
    
    def __str__(self):
        return f"Shipping Address - {self.shipping_full_name} - City: {self.shipping_city}"
    

# Create a user Shipping Address by default when user signup
def create_shipping(sender,instance, created, **kwargs):
    if created:
        user_shipping=ShippingAddress(user=instance)
        user_shipping.save()
        
# Automate the Shipping thing  
post_save.connect(create_shipping,sender=User)      
    
    
    
# Create Oder Model 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    shipping_address = models.CharField(max_length=1500)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped=models.BooleanField(default=False)
    date_shipped=models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return f'Order - {self.id}'
    
    
    
# Auto Add Shipping Date    
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now=datetime.datetime.now()
        obj=sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped=now   
    
    
    
# Create Oder  Item Model 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity=models.PositiveBigIntegerField(default=1)
    price=models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
        return f'Order Item - {str(self.id)}'  
        
        
    


