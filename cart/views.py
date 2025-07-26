from django.shortcuts import render, redirect
from store.models import Product
from . models import Cart, CartItem 
from django.db.models import Q

# Create your views here.

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def cart(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
    else: # Guest user
        session_id = get_create_session(request) # Get or create session ID
        cartid = Cart.objects.get(cart_id = session_id)
        cart_id = Cart.objects.filter(cart_id=session_id).exists()
        
        if cart_id:
            cart_items = CartItem.objects.filter(cart=cartid)
            for item in cart_items:
                total += item.product.price * item.quantity
    
    tax = (total * 1) / 100
    grand_total = total + tax
        
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'tax': tax, 'total': total, 'grand_total': grand_total})



def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = get_create_session(request)

    if request.user.is_authenticated:  # Logged-in user
        cart_item_qs = CartItem.objects.filter(product=product, user=request.user)
        if cart_item_qs.exists():
            item = cart_item_qs.first()
            item.quantity += 1
            item.save()
        else:
            cartid = Cart.objects.get_or_create(cart_id=session_id)[0]
            CartItem.objects.create(
                cart=cartid,
                product=product,
                quantity=1,
                user=request.user
            )
    else:  # Guest user
        cartid, _ = Cart.objects.get_or_create(cart_id=session_id)
        cart_item_qs = CartItem.objects.filter(product=product, cart=cartid)

        if cart_item_qs.exists():
            item = cart_item_qs.first()
            item.quantity += 1
            item.save()
        else:
            CartItem.objects.create(
                cart=cartid,
                product=product,
                quantity=1
            )

    return redirect('cart')




def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = request.session.session_key
    cartid = Cart.objects.get(cart_id=session_id)
    cart_item = CartItem.objects.get(cart=cartid, product=product)
    # print(cart_item)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')


def remove_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = request.session.session_key
    cartid = Cart.objects.get(cart_id=session_id)
    cart_item = CartItem.objects.get(cart=cartid, product=product)
    
    cart_item.delete()
    
    return redirect('cart')


    