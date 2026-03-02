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
        if str(prod['id']) == cart[str(prod['id'])]:
            quantity += cart[str(prod['id'])]
            total += cart[str(prod['id'])] * prod['price']
            prods.append({
                        'id' : prod['id'],
                        'prod' : prod['name'],
                        'image' : prod['image'],
                        'quantity' : cart[str(prod['id'])],
                        'tot' : cart[str(prod['id'])] * prod['price']
                        })
                    
    
    context = {
        'products' :prods,
        'total' : total,
        'cart_count' : quantity,
    }
    
    return render(request, 'restaurant/cart.html', context)
    
def update_cart(request):
    cart = request.POST.get("cart",{})
    ...
    request.session['cart']=cart
    request.session.modified = True
    return
def add_to_cart(request):
    ...


    
