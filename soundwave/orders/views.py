from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from cart.models import Cart,Cartitem
from user.models import CustomUser
from accounts.models import Address
from .models import Order,Order_items
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from . models import Order_items


# Create your views here. 

@never_cache
@login_required(login_url='user_login')
def checkout(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_items = cart.items.all()
    addresses = Address.objects.filter(user=user)

    if request.method == 'POST':
        address_id = request.POST.get('selected_address')  
        payment_method = request.POST.get('payment_method')
        
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=user)
            
            order = Order.objects.create(
                user=user,
                shipping_address=address,
                payment_type=payment_method,
                total_price=cart.total_price
            )
            
            for item in cart_items:
                Order_items.objects.create(
                    order=order,
                    variant=item.variant, 
                    quantity=item.quantity,
                    price=item.variant.product.price,
                    subtotal_price=item.variant.product.price * item.quantity
                )

            cart.items.all().delete()

            messages.success(request, 'Your order has been placed successfully.')
            return redirect('order_confirmation')
        else:
            messages.error(request, 'Please select a valid shipping address.')

    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total': cart.total_price})


def order_confirm(request):
    
    return render(request,'user/order_confirmation.html')

@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def view_orders(request):
    orders=Order_items.objects.select_related('order','variant__product','order__user','order__shipping_address')
    return render(request,'admin/orders.html',{'orders':orders})

@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def change_order_status(request, order_item_id, new_status):
    order_item = get_object_or_404(Order_items, Orderitem_id=order_item_id)
    order_item.status = new_status
    order_item.save()
    return redirect('view_orders') 
