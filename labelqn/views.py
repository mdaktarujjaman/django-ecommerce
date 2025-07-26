from django.shortcuts import render
from store.models import Product

def home(request):
    product = Product.objects.all().order_by('-created_date')[:8]
    
    return render(request, 'index.html', {'products': product})