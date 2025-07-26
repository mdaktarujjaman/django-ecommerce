from django.shortcuts import render, redirect
from cart.models import Cart, CartItem 
from . forms import OrderForm
from . ssl import sslcommerz_payment_gateway

# Create your views here.
def order_complete(request):
    return render(request, 'orders/order_complete.html')



def place_order(request):
    print(request.POST)
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    
    if cart_items.count()<1:
        return redirect('store')
    for item in cart_items:
        total += item.product.price * item.quantity
    
    tax = (total * 1) / 100
    grand_total = total + tax
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    }
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.tax = tax
            form.instance.order_total = grand_total
            form.instance.ip = request.META.get('REMOTE_ADDR')
            saved_instance = form.save()
            form.instance.order_number = saved_instance.id
            form.save()
            print('form print',form)
            return redirect(sslcommerz_payment_gateway(request))
    return render(request, 'orders/place-order.html', context)

