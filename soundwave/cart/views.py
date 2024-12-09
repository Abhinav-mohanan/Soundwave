from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart,Cartitem
from products.models import Variant
from django.views.decorators.cache import never_cache




#=====================Cart managment=======================#
@never_cache
@login_required(login_url='user_login')
def add_to_cart(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = Cartitem.objects.get_or_create(cart=cart, variant=variant)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


@never_cache
@login_required
def remove_from_cart(requet,cartitem_id):
    cart_item=get_object_or_404(Cartitem,cartitem_id=cartitem_id,cart__user=requet.user)
    cart_item.delete()
    return redirect('cart_detail')


@never_cache
@login_required 
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(Cartitem, cartitem_id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart_item.quantity = quantity
        cart_item.save()
        response_data = {
            'total_price': cart_item.total_price,
            'total_cart_price': cart_item.cart.total_price,
        }
        return JsonResponse(response_data)


@never_cache
@login_required(login_url='user_login')
def cart_detil(request):
    cart=get_object_or_404(Cart,user=request.user)
    cart_items=cart.items.all()
    total=cart.total_price
    return render(request,'user/cart.html',{'cart_items':cart_items,'total':total})


@never_cache
@login_required
def update_cart_quantity(request, cartitem_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cartitem, cartitem_id=cartitem_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity'))
        cart_item.quantity = quantity
        cart_item.save()
        response_data = {
            'total_price': cart_item.total_price,
            'total_cart_price': cart_item.cart.total_price,
        }
        return JsonResponse(response_data)


