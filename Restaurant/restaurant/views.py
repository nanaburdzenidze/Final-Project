from django.shortcuts import render, redirect
import requests

API_BASE = "https://restaurant.stepprojects.ge"

def filter_by_cat(request):
    filtered=[]
    sel_category = request.GET.get('category')
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    if not sel_category:
        return products
    
    for prod in products:
        if str(prod['categoryId']) == sel_category:
            filtered.append(prod)
    return filtered

def filter_by_preference(request, prods):
    filtered = []
    vegetarian = request.GET.get('vegetarian')
    nuts = request.GET.get('nuts')
    spiciness = request.GET.get('spicy')
    for prod in prods:
        if vegetarian == '1' and not prod['vegetarian']:
             continue
        if nuts == '1' and not prod['nuts']:
            continue
        if spiciness == '0' and not (prod['spiciness'] == 0 ):
            continue
        if spiciness == '1' and not (prod['spiciness'] == 1 ):
            continue
        if spiciness == '2' and not (prod['spiciness'] == 2 ):
            continue
        if spiciness == '3' and not (prod['spiciness'] == 3 ):
            continue
        if spiciness == '4' and not (prod['spiciness'] == 4 ):
            continue
        filtered.append(prod)
    return filtered
       
       
def index(request):
    categories = requests.get(f"{API_BASE}/api/Categories/GetAll").json()
    products = filter_by_cat(request)
    products = filter_by_preference(request, products)
    context = {
        'categories' : categories,
        'products' : products,
    }
    
    return render(request, 'restaurant/index.html', context)
        
def cart(request):
    cart = request.session.get('cart',{})
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    
    prods = []   
    quantity = 0
    total = 0
    
    '''
    პროდუქტებში ვეძებთ ისეთებს რომლებიც არი კალათაში, ვითვლით მათ რაოდენობას, ფასს ვქმნით ახალ ლისტს ლექსიკონებისას
    '''
    for prod in products :
        if str(prod['id']) in cart:
            quantity += cart[str(prod['id'])]
            total += cart[str(prod['id'])] * prod['price']
            prods.append({
                        'id' : prod['id'],
                        'prod' : prod['name'],
                        'image' : prod['image'],
                        'quantity' : cart[str(prod['id'])],
                        'price': prod['price'],
                        'tot' : cart[str(prod['id'])] * prod['price']
                        })
                    
    
    context = {
        'products' :prods,
        'total' : total,
        'cart_count' : quantity,
    }
    
    return render(request, 'restaurant/cart.html', context)
    
def update_cart(request):
    cart = request.session.get('cart',{})
    ...
    request.session['cart']=cart
    request.session.modified = True
    return redirect('menu')

def add_to_cart(request):
    #ვიღებთ მიმდინარე კალატასა და პროდუქტს რომლის დამატებაც გვინდა კალათაში
    cart = request.session.get('cart',{})
    prod = request.POST.get('product_id')
    #ვამოწმებთ არის თუ არა ის უკვე კალათაში, თუ არის მის რაოდენობას გავზრდით ერთით თუ არადა ახალი რპდუქტი უნდა დაემატოს კალათას
    if prod in cart:
        cart[prod] += 1
    else:
        cart[prod] = 1
    request.session['cart']=cart
    request.session.modified = True
    return redirect('menu')


    
