from django.shortcuts import render, redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignupForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Q
from cart.cart import Cart
import json
from payment.forms import ShippingForm
from payment.models import ShippingAddress

# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html')



def register_user(request):
    form=SignupForm()
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login is User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created-Please Fill Out Your User Info Below!")
            return redirect('update_info')
        else:
            messages.success(request, 'You Have a Problem Register! Please Try Again')
            return redirect('register')
    else:    
        return render(request, 'register.html', {'form': form})  



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Shopping Cart Logic
            current_user, created = Profile.objects.get_or_create(user=request.user)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, 'Logged In Successfully!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error, Please Try Again!')
            return redirect('login')
    else:
        return render(request, 'login.html') 




def logout_user(request):
    logout(request)
    messages.success(request, 'Logedout Successfully!')
    return redirect('home')



def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def category(request, cat):
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, 'Category does not exist')
        return redirect('home')
    



def category_summary(request): 
    categories=Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})   



def update_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = UpdateUserForm(instance=request.user)
        return render(request, 'update_user.html', {'user_form': form})
    else:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')
    
    
    
def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, request.user)  
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('update_password')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ChangePasswordForm(request.user)
        
        return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('home')   
    
    
    

def update_info(request):
    if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)
        # Shipping Info
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id)
        form=UserInfoForm(request.POST or None, instance=current_user)
        # Shipping Form
        shipping_form =ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            # Save Shipping Form
            shipping_form.save()
            messages.success(request, 'Your Info has been updated successfully.')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'Your must be logged in to Access That Page!')
        return redirect('home') 

        
        

def search(request):
    if request.method=="POST":
        searched=request.POST['searched']
        searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, 'This Product Does Not Exists, plz try again!!')
            return render(request, 'search.html')
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html')   
    
    
    








