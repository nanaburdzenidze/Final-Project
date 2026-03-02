from django.shortcuts import render
import requests

API_BASE = "https://restaurant.stepprojects.ge"
def index(request):
    categories = requests.get(f"{API_BASE}/api/Categories/GetAll").json()
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    sel_category = request.GET.get('category')
    context = {
        'categories' : categories,
        'products' : products,
        #'prod_count' : count,
    }
    
    return render(request, 'restaurant/index.html', context)
        
def cart(request):
    cart = request.session.get('cart',{})
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    prods = []   
    quantity = 0
    total = 0
        for prod in products :
            if str(prod['id']) == cart['id']:
                total += prod[id].price * cart['id']
                prods.append(prod)
                quantity += 1
                    
    
    context = {
        'products' = prods
        'quantity' = quantity
        'price' = 
        'total' = total
        'cart_count' =
    }
    
    ...
    
def update_cart(request):
    cart = request.POST.get("cart",{})
    ...
    request.session['cart']=cart
    request.session.modified = True
    return
def add_to_cart(request):
    ...


    
