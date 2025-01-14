from store.models import Product,Profile

class Cart():
    def __init__(self, request):
        self.session=request.session
        # Get Request
        self.request=request
        #Get the current session key if it exists
        cart=self.session.get('session_key')
        # If User is new!no session key
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        # Cart is avalable is Page
        self.cart=cart
        
    
    def db_add(self, product, quantity):
        product_id=str(product)    
        product_qty=str(quantity)    
        # Logic
        if product_id in self.cart:
            pass    
        else:
            # self.cart[product_id]   ={'price': str(product.price)} 
            self.cart[product_id]   = int(product_qty)
        self.session.modified=True 
        
        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            carty=str(self.cart)
            carty=carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))     
        
    
    
    
    def add(self, product, quantity):
        product_id=str(product.id)    
        product_qty=str(quantity)    
        # Logic
        if product_id in self.cart:
            pass    
        else:
            # self.cart[product_id]   ={'price': str(product.price)} 
            self.cart[product_id]   = int(product_qty)
        self.session.modified=True 
        
        # # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            carty=str(self.cart)
            carty=carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty)) 
        
        
        
    def cart_total(self):
        # Get Product IDS 
        product_ids=self.cart.keys()   
        products=Product.objects.filter(id__in=product_ids) 
        # Get Quantities  
        quantities=self.cart
        total=0 
        
        for key,value in quantities.items():
            key=int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total=total + (product.sale_price * value)
                    else:    
                        total=total + (product.price * value)
        return total
        
    
    
    def __len__(self):
        return len(self.cart)  
    
    
    def get_products(self):
        # Get Ids from cart
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        return products  
    
    def get_quantities(self):
        quantities=self.cart
        return quantities
    
    def update(self, product,quantity):
        product_id=str(product)    
        product_qty=int(quantity)
        
        # Get Cart
        ourcart=self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty
        
        self.session.modified=True 
        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            carty=str(self.cart)
            carty=carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
        thing=self.cart    
        return thing


        
    def delete(self, product):
        product_id=str(product)    
        # Delete From Dictonary Cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True
        
        
        
        
        
            
                     
    