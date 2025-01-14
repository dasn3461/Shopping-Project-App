from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm 
from .models import ShippingAddress,Order,OrderItem
from django.contrib import messages 
from store.models import Product,Profile
import datetime


# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as a logged-in user
        # Retrieve or create a new ShippingAddress for the authenticated user
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        # Create the shipping form using the retrieved or newly created address instance
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        # Checkout as guest (no associated user)
        shipping_form = ShippingForm(request.POST or None)

    return render(request, 'payment/checkout.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form
    })
    


def billing_info(request):  
    if request.POST:
        cart=Cart(request)
        cart_products=cart.get_products
        quantities=cart.get_quantities
        totals=cart.cart_total()
        
        # Create a session with Shipping Info 
        my_shipping=request.POST 
        request.session['my_shipping']=my_shipping
        
        
        # Check to see if user in Logged In
        if request.user.is_authenticated:
            # Get Billing Form
            billing_form=PaymentForm()
            return render(request, 'payment/billing_info.html',{'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        
        else:
            # Get Billing Form
            billing_form=PaymentForm()
            return render(request, 'payment/billing_info.html',{'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        shipping_form =request.POST 
        return render(request, 'payment/billing_info.html',{'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
    
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
    
   
    
def process_order(request):  
    if request.POST:
        cart=Cart(request)
        cart_products=cart.get_products
        quantities=cart.get_quantities
        totals=cart.cart_total()
        # Get Billing Info From the last page
        payment_form=PaymentForm(request.POST or None) 
        # Get Shipping Session Data 
        my_shipping=request.session.get('my_shipping')
        
        # Gather Oder Info
        full_name=my_shipping['shipping_full_name']
        email=my_shipping['shipping_email']
        
        
        # Create Shipping Address from session Info
        shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_division']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid=totals
        
         # Create an Order
        if request.user.is_authenticated:
            # Logged In
            user=request.user
            # Create Order
            create_order=Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            # Get the Order ID
            order_id=create_order.pk
            # Get Product Info
            for product in cart_products():
                product_id=product.id
                # Get Product Price
                if product.is_sale:
                      price=product.sale_price
                else:     
                    price=product.price 
                
                # Get Quantity
                for key, value in quantities().items():
                    if int(key)  == product.id:
                        #Create Order  Item 
                        create_order_item =OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value, price=price)
                        create_order_item.save()
                
                #  Delete our cart     
            for key in list(request.session.keys()):
                if key == "session_key":
                    #Delete Key
                    del request.session[key]      
                            
            messages.success(request, 'Order Placed!')
            return redirect('home')
        
        else:
            # Not Logged In
            # Create  Order
            create_order=Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()  
            
            # Add Order Items
            # Get the Order ID
            order_id=create_order.pk
            # Get Product Info
            for product in cart_products():
                product_id=product.id
                # Get Product Price
                if product.is_sale:
                    price=product.sale_price
                else:    
                    price=product.price
                
                # Get Quantity
                for key, value in quantities().items():
                    if int(key)  == product.id:
                        #Create Order  Item 
                        create_order_item =OrderItem(order_id=order_id,product_id=product_id,quantity=value, price=price)
                        create_order_item.save()
                        
                #  Delete our cart     
            for key in list(request.session.keys()):
                if key == "session_key":
                    #Delete Key
                    del request.session[key]     
                    
                    
            #   Delete Cart from Database     
            current_user=Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database
            current_user.update(old_cart="")
            
            
            messages.success(request, 'Order Placed!')
            return redirect('home')
        
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
    
    

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.method == 'POST':
            num = request.POST.get('num')
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, 'Access Denied')
        return redirect('home')  



def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.method == 'POST':
            num = request.POST.get('num')
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)
            order.update(shipped=True, date_shipped=now)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, 'Access Denied')
        return redirect('home')
    
    
    
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status=request.POST['shipping_status']
            if status =="true":
                order=Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order=Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, 'Shipping Status Updated')   
            return redirect('home') 
                    
        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    
    
    else:
        messages.error(request, 'Access Denied')
        return redirect('home')   
    
    
          
     