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
from accounts.form import Addressform
from products.models import Product,Variant
from offer.models import Product_offer,Brand_offer
from django.utils.timezone import now
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here. 


@never_cache
@login_required(login_url='user_login')
def checkout(request):
    user=request.user
    cart=get_object_or_404(Cart,user=user)
    cart_items=Cartitem.objects.filter(cart=cart)
    addresses=Address.objects.filter(user=user,is_active=True)
    current_date=now().date()
    
    for cart_item in cart_items:
        variant=cart_item.variant
        product=variant.product

        if product.is_listed==False:
            messages.error(request,'Remove unavialable product')
            return redirect('cart_detail')
        
        if product.category.is_listed==False:
            messages.error(request,'Remove unavailable product')
            return redirect('cart_detail')
        

        for cart_item in cart_items:
            variant=get_object_or_404(Variant,id=cart_item.variant.id)

        if variant.stock == 0:
            messages.error(request,'Please remove outof stock product')
            return redirect('cart_detail')
        
        product_offer=Product_offer.objects.filter(
            product=product,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        brand_offer=Brand_offer.objects.filter(
            brand=product.brand,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        product_discount_price=(product.price * (1-(product_offer.offer_percentage/100))) if product_offer else None
        brand_discount_price=(product.price* (1-brand_offer.offer_percentage/100)) if brand_offer else None

        if product_discount_price is not None and brand_discount_price is not None:
            final_discount_price=min(product_discount_price,brand_discount_price)
        elif product_discount_price is not None:
            final_discount_price=product_discount_price
        elif brand_discount_price is not None:
            final_discount_price=brand_discount_price
        else:
            final_discount_price=product.price

        final_discount_price=round(final_discount_price,0)
        cart_item.variant.product.price =final_discount_price

        total=sum(item.total_price for item in cart_items)
        
        
    for item in cart_items:
        if item.quantity >item.variant.stock:
            messages.error(request,f'{item.variant.product.name} {item.variant.color} is exceeds available stock')
            return redirect('cart_detail') 
        
    
    form=Addressform()
    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total': total,'form':form})



@never_cache
@login_required
def checkout_address(request):
    if request.method == 'POST':
        form = Addressform(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user  
            address.save()
            messages.success(request, 'Your address has been added successfully')
            return redirect('checkout')  
        else:
            print(form.errors)
            messages.error(request, 'Please correct the form and try again.')
            return redirect('checkout')
        



@never_cache
@login_required(login_url='user_login')
def order_confirm(request): 
    return render(request,'user/order_confirmation.html')


@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def view_orders(request):
    orders=Order_items.objects.select_related('order','variant__product','order__user','order__shipping_address').order_by('-order__created_at')
    status_filter=request.GET.get('status')
    if status_filter:
        orders=orders.filter(status=status_filter)
    return render(request,'admin/orders.html',{'orders':orders})


@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def change_order_status(request, order_item_id, new_status):
    order_item = get_object_or_404(Order_items, Orderitem_id=order_item_id)
    order_item.status = new_status
    order_item.save()
    return redirect('view_orders') 





@login_required(login_url='user_login')
def place_order(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_items = Cartitem.objects.filter(cart=cart)
    addresses = Address.objects.filter(user=user)

    if request.method == 'POST':
        address_id = request.POST.get('selected_address')  
        payment_method = request.POST.get('payment_method')

        if address_id:
            address = get_object_or_404(Address, id=address_id, user=user)

        if payment_method == 'COD':
            payment_status = 'Pending'
            order = Order.objects.create(
                user=user,
                shipping_address=address,
                payment_type=payment_method,
                total_price=cart.total_price,
                payment_status=payment_status,
            )
            
            for item in cart_items:
                Order_items.objects.create(
                    order=order,
                    variant=item.variant, 
                    quantity=item.quantity,
                    price=item.variant.product.price,
                    subtotal_price=item.variant.product.price * item.quantity
                )

            cart_items.delete()
            messages.success(request, 'Your order has been placed successfully.')
            return redirect('order_confirmation')

        elif payment_method == 'RazorPay':
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                'amount': int(cart.total_price * 100),  # amount in paise
                'currency': 'INR',
                'payment_capture': '1',
            })
            razorpay_order_id = razorpay_order['id']
            return render(request, 'user/razorpay_payment.html', {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'total': cart.total_price,
            })

    form = Addressform()
    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total': cart.total_price, 'form': form})


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature(params_dict)

            # Payment verified successfully
            order = Order.objects.create(
                user=request.user,
                payment_type='RazorPay',
                total_price=request.POST.get('total'),
                payment_status='Success',
                shipping_address=None,  # Adjust as necessary
            )

            # Process the cart items
            cart = Cart.objects.get(user=request.user)
            cart_items = Cartitem.objects.filter(cart=cart)
            for item in cart_items:
                Order_items.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.product.price,
                    subtotal_price=item.variant.product.price * item.quantity
                )
            cart_items.delete()

            messages.success(request, 'Payment successful. Order placed!')
            return redirect('order_confirmation')

        except razorpay.errors.SignatureVerificationError:
            messages.error(request, 'Payment verification failed.')
            return redirect('checkout')


