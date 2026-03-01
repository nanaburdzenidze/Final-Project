from django.shortcuts import render
import requests

API_BASE = "https://restaurant.stepprojects.ge"
def index(request):
    categories = requests.get(f"{API_BASE}/api/Categories/GetAll").json()
    products = requests.get(f"{API_BASE}/api/Products/GetAll").json()
    sel_category = request.GET.get('category')
    if sel_category is None:
        ...
    
    
    context = {
        'categories' : categories,
        'products' : products,
        #'prod_count' : count,
    }
    
    return render(request, 'restaurant/index.html', context)
        
def cart_page(request):
    ...

    
