from django.shortcuts import render, redirect
import requests

API_BASE = "https://restaurant.stepprojects.ge"

'''
მივიღებთ ინფორმაცია თუ რომელი კატეგორიაა მონიშნული, მონიშნული კატეგორიის მიხედვით გდავუყვებით ყველა პროდუქტს 
და სიაში ჩავაგდებთ მხოლოდ ისეთებს რომლის კატეგორია ემთხვევა მონიშნულ კატეგროიას
'''
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

'''
გადმოგვეცემა პროდუქტების სია, ასევე ვიგებთ მონიშნული არის თუ არა ვეგეტარიანული და თხილით, ვიგებთ სიცხარის დონეს რომელიც მონიშნულია.
ამის შემდეგ ვფილტავრთ გადმოცემულ პრდოუქტებს.
'''
def filter_by_preference(request, prods):
    filtered = []
    vegetarian = request.GET.get('vegetarian')
    nuts = request.GET.get('nuts')
    spiciness = request.GET.get('spicy')
    any_spiciness = request.GET.get('any')
    for prod in prods:
        if vegetarian == '1' and not prod.get('vegetarian',False):
             continue
        if nuts == '1' and not prod.get('nuts',False):
            continue
        if not any_spiciness:
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
       
'''
ვიღებთ კატეგორიებს , ვფილტრავთ პროდუქტებს კატეგორიების მიხედვით( თუ კატეგორია არ არის მონიშნული გვენმქბეა ყველა პროდუქტი) შემდეგ კი ვფილტრავთ პრეფერენსების მიხედვით.
'''      
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
    cart = requests.get(f"{API_BASE}/api/Baskets/GetAll").json()
    
    prods = []   
    quantity = 0
    total = 0
    
    '''
    პროდუქტებში ვეძებთ ისეთებს რომლებიც არი კალათაში, ვითვლით მათ რაოდენობას, ფასს ვქმნით ახალ ლისტს ლექსიკონებისას
    '''
    for prod in cart :
        quantity += prod['quantity']
        total += prod['quantity'] * prod['price']
        prods.append({
                    'id' : prod.get('id'),
                    'productId': prod['product']['id'],
                    'prod' : prod['product']['name'],
                    'image' : prod['product']['image'],
                    'quantity' : prod['quantity'],
                    'price': prod['price'],
                    'tot' : prod['quantity'] * prod['price']
                    })
                    
    context = {
        'products' :prods,
        'total' : total,
        'cart_count' : quantity,
    }
    
    return render(request, 'restaurant/cart.html', context)
    
    
def update_cart(request):
    action = request.POST.get('action')
    prod_id = int(request.POST.get('product_id'))
    quantity =0
    price = 0
    cart = requests.get(f"{API_BASE}/api/Baskets/GetAll").json()
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    if action == 'remove': 
        requests.delete(f"{API_BASE}/api/Baskets/DeleteProduct/{prod_id}")
        return redirect('cart')
    for prod in products:
        if prod['id'] == prod_id:
            price = prod['price']
            break
    for prod in cart:
        if int(prod['product']['id']) == prod_id:
            quantity = int(prod['quantity'])
            break
         
        
    if action == 'reduce':
        if quantity >1:
            quantity -= 1
        else:
            requests.delete(f"{API_BASE}/api/Baskets/DeleteProduct/{prod_id}")
            return redirect('cart')
    elif action == 'add':
        quantity += 1
    requests.put(f"{API_BASE}/api/Baskets/UpdateBasket", json={'productId':prod_id,'quantity':quantity, 'price': price})
    return redirect('cart')

def add_to_cart(request):
    prod_id = int(request.POST.get('product_id'))
    cart = requests.get(f"{API_BASE}/api/Baskets/GetAll").json()
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    price = 0

    for p in cart:
        if (p['product']['id']) == prod_id:
            quantity = p['quantity']+1
            requests.put(f"{API_BASE}/api/Baskets/UpdateBasket", json={ 'productId':prod_id,'quantity': quantity, 'price':p['price']})
            return redirect('menu')
    for p in products:
        if p['id'] == prod_id:
            price = p['price']
            
            break
    requests.post(f"{API_BASE}/api/Baskets/AddToBasket", json={'productId': prod_id, 'quantity': 1,'price':price})
    return redirect('menu')