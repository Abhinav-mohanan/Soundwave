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
from django.http import JsonResponse,HttpResponse
from xhtml2pdf import pisa
from coupon.models import Couponusage,Coupon
from wallet.models import Wallet,Transaction
from decimal import Decimal
from django.db.models import F
from django.db import transaction
from wallet.models import Wallet,Transaction

# Create your views here. 

#======================Checkout page=====================# 
@never_cache
@login_required(login_url='user_login')
def checkout(request):
    user=request.user
    cart=get_object_or_404(Cart,user=user)
    cart_items=Cartitem.objects.filter(cart=cart)
    addresses=Address.objects.filter(user=user,is_active=True)
    current_date=now().date()
    total=0

    if not cart_items.exists():
        return redirect('cart_detail')

    for cart_item in cart_items:
        variant=cart_item.variant
        product=variant.product

        if not product.is_listed:
            messages.error(request,'Remove unavailable product')
            return redirect('cart_detail')
        
        if not product.category.is_listed:
            messages.error(request,'Remove unavailable product')
            return redirect('cart_detail')
        
        if not product.brand.is_listed:
            messages.error(request,'Remove unavailable Product')
            return redirect('cart_detail')
        
        if not product.subcategory.is_listed:
            messages.error(request,'Remove unavailable Product')
            return redirect('cart_detail')

        if variant.stock == 0:
            messages.error(request,'Please remove outof stock product')
            return redirect('cart_detail')
        if variant.is_listed==False:
            messages.error(request,'Please remove unavailable Product')
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
        
        cart_item.variant.product.price=round(final_discount_price,0)

    total=round(sum(item.total_price for item in cart_items),0)
    for item in cart_items:
        if item.quantity >item.variant.stock:
            messages.error(request,f'{item.variant.product.name} {item.variant.color} is exceeds available stock')
            return redirect('cart_detail') 
        
    coupons=Coupon.objects.filter(is_active=True)
        
    
    form=Addressform()
    wallet=Wallet.objects.filter(user=user).first()
    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total': total,'form':form,'coupons':coupons,'wallet':wallet})


#======================Checkout page End========================# 


#=====================Checkout Address section===================# 
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
            
            messages.error(request, 'Please correct the form and try again.')
            return redirect('checkout')
        
#======================Checkout_Address section End=====================# 


#======================Admin_order Managment=====================# 
@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def view_orders(request):
    orders=Order.objects.all()
    return render(request,'admin/orders.html',{'orders':orders})


@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def change_order_status(request, order_item_id, new_status):
    order_item = get_object_or_404(Order_items, Orderitem_id=order_item_id)
    order = order_item.order
    user_wallet, _ = Wallet.objects.get_or_create(user=order.user)
    current_date=now().date()
    product=order_item.variant.product
    brand=product.brand

    product_offer=Product_offer.objects.filter(
        product=product,
        started_date__lte=current_date,
        end_date__gte=current_date,
        status=True
    ).first()

    brand_offer=Brand_offer.objects.filter(
        brand=brand,
        started_date__lte=current_date,
        end_date=current_date,
        status=True
    ).first()

    product_discount_price=None
    brand_disount_price=None

    if product_offer:
        product_discount_price=round(product.price * (1-(product_offer.offer_percentage/100)))

    if brand_offer:
        brand_disount_price=round(product.price * (1-(product_offer.offer_percentage/100)))

    if product_discount_price is not None and brand_disount_price is not None:
            final_price=min(product_discount_price,brand_disount_price)
    elif product_discount_price is not None:
            final_price=product_discount_price
    elif brand_disount_price is not None:
        final_price=brand_disount_price
    else:
        final_price=product.price

    refund_amount=Decimal(final_price * order_item.quantity)

    if order.coupon_price>0:
        coupon_refund = (order_item.subtotal_price/order.total_price) * order.coupon_price
    else:
        coupon_refund =Decimal(0)

    if new_status == 'Returned' and order_item.status == 'Requested Return':
        with transaction.atomic():
            order_item.status = new_status
            order_item.save()

            user_wallet.balance += refund_amount
            user_wallet.save()

            if coupon_refund>0:
                Transaction.objects.create(
                    wallet=user_wallet,
                    details=f'Coupon Refund for Order Item {order.tracking_number}',
                    amount= coupon_refund,
                    transaction_type='Credit'
                )

            Transaction.objects.create(
                wallet=user_wallet,
                details=f"Refund for Order Item {order.tracking_number}",
                amount=(refund_amount- coupon_refund),
                transaction_type='Credit'
            )

            messages.success(
                request,
                f"Refund of ₹{refund_amount - coupon_refund} credited to {order.user.username}'s wallet."
            )
    elif new_status == 'Cancelled' and order_item.status == 'Requested Return':
        order_item.status = 'Request Rejected'
        order_item.save()
        messages.info(request, f"The return request for order item {order_item.variant.product.name} has been rejected.")
    else:
        order_item.status = new_status
        order_item.save()
    order_items=order.order_items.all()
    return render(request,'admin/order_items.html',{'order':order,'order_items':order_items})



@never_cache
@user_passes_test(lambda u :u.is_superuser,login_url='/adminn/')
def orderitems_detail(request,order_id):
    order=get_object_or_404(Order,order_id=order_id)
    order_items=order.order_items.all()
    return render(request,'admin/order_items.html',{'order':order,'order_items':order_items})


#==================Admin_order Managment End==================# 



#=======================Place order===========================# 
@login_required(login_url='user_login')
def place_order(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_items = Cartitem.objects.filter(cart=cart)
    addresses = Address.objects.filter(user=user)
    current_date=now().date()
    total_offer_price=0
    total_price=0
    coupon_discount=0
    final_discount_price=0
    offer_price=0
    coupon=request.session.get('applied_coupon_id') 

    if not cart_items.exists():
        return redirect('cart_detail')


    for cart_item in cart_items:
        variant=cart_item.variant
        product=variant.product

       

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
        product_discount_price=None
        brand_discount_price=None

        if product_offer:
            product_discount_price = (product.price * (1-(product_offer.offer_percentage/100)))
        
        if brand_offer:
            brand_discount_price=(product.price* (1-(brand_offer.offer_percentage/100)))

        if product_discount_price is not None and brand_discount_price is not None:
            final_discount_price=min(product_discount_price,brand_discount_price)
        elif product_discount_price is not None:
            final_discount_price =product_discount_price
        elif brand_discount_price is not None:
            final_discount_price= brand_discount_price
        else:
            final_discount_price=product.price

        offer_price=product.price - final_discount_price
        cart_item.variant.product.price =final_discount_price
    
    total_price=sum(item.total_price for item in cart_items)
        

   
    applied_coupon_id=request.session.get('applied_coupon_id')
    
    if applied_coupon_id:
        try:
            coupon=Coupon.objects.get(coupon_id=applied_coupon_id)
            total_offer_price = sum(cart_item.variant.product.price * cart_item.quantity for cart_item in cart_items)
            if coupon.coupon_type=='fixed':
                coupon_discount=min(coupon.discount_amount,total_offer_price)
            elif coupon.coupon_type=='percentage':
                coupon_discount=total_offer_price*(coupon.discount_amount/100)
            else:
                coupon_discount=0  
                if 'applied_coupon_id' in request.session:
                    del request.session['applied_coupon_id']
        except Coupon.DoesNotExist:
            coupon_discount=0
    total_price-=coupon_discount
    total_price=round(total_price,0)

    if request.method == 'POST':
        address_id = request.POST.get('selected_address')  
        payment_method = request.POST.get('payment_method')

        if address_id:
            address = get_object_or_404(Address, id=address_id, user=user)
        else:
            messages.error(request,'Please select a address and countinue')
            return redirect('checkout')

        if payment_method == 'COD':
            payment_status = 'Pending'
            order = Order.objects.create(
                user=user,
                shipping_address=address,
                payment_type=payment_method,
                total_price=total_price,
                payment_status=payment_status,
                offer_price=offer_price,
                coupon_price=coupon_discount          
            )
            
            for item in cart_items:
                Order_items.objects.create(
                    order=order,
                    variant=item.variant, 
                    quantity=item.quantity,
                    price=item.variant.product.price,
                    subtotal_price=(item.variant.product.price * item.quantity)-coupon_discount
                )

                item.variant.stock-=item.quantity
                item.variant.save()


            cart_items.delete()
            if coupon:
                Couponusage.objects.create(user=user,coupon=coupon,is_used=True)
                coupon.usage_limit+=1
                coupon.save()
            if 'applied_coupon_id' in request.session:
                del request.session['applied_coupon_id']
            messages.success(request, 'Your order has been placed successfully.')
            return redirect('order_confirmation')

        elif payment_method == 'RazorPay':
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                'amount': int(total_price * 100),  
                'currency': 'INR',
                'payment_capture': '1',
            })
            razorpay_order_id = razorpay_order['id']
            request.session['pending_order_details']={
                'user':user.id,
                'shipping_address_id':address.id,
                'payment_type':payment_method,
                'total_price':float(total_price),
                'coupon_id':coupon.coupon_id if coupon else None,
                'coupon_price':float(coupon_discount),
                'offer_price':float(offer_price)


            }
            return render(request, 'user/razorpay_payment.html', {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'total': total_price,
            })
        elif payment_method =='wallet':
            wallet,created=Wallet.objects.get_or_create(user=user)
            if wallet:
                if wallet.balance < total_price:
                    messages.error(request,'Insufficient balance in your Wallet please choose anthor payment methode.')
                else:
                    payment_status='Success'
                    order=Order.objects.create(
                        user=user,
                        shipping_address=address,
                        total_price=total_price,
                        payment_type=payment_method,
                        payment_status=payment_status,
                        offer_price=offer_price,
                        coupon_price=coupon_discount
                    )
                    for item in cart_items:
                        Order_items.objects.create(
                            order=order,
                            variant=item.variant,
                            quantity=item.quantity,
                            price=item.variant.product.price,
                            subtotal_price=(item.variant.product.price * item.quantity)-coupon_discount
                        )
                    wallet.balance-=total_price
                    wallet.save()
                    Transaction.objects.create(
                    wallet=wallet,
                    transaction_type='Debit',
                    amount=total_price,
                    details=f'The {total_price} is debited for the order {order.tracking_number}'
                    )
                    item.variant.stock-=item.quantity
                    item.variant.save()
                    cart_items.delete()
                    if coupon:
                        Couponusage.objects.create(user=user,coupon=coupon,is_used=True)
                        coupon.usage_limit+=1
                        coupon.save()

                    if 'applied_coupon_id' in request.session:
                        del request.session['applied_coupon_id']
                    messages.success(request,'Your Order has been placed Successfuly')
                    return redirect('order_confirmation')
                

    coupons=Coupon.objects.filter(is_active=True)
    form = Addressform()
    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total': cart.total_price, 'form': form,'coupons':coupons})


#=======================Place order End===========================# 


#=====================Verify razorpay payment=====================# 
@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_status = 'Failure'
        coupon_discount=0
        try:
            client.utility.verify_payment_signature(params_dict)
            payment_status = 'Success'

            order_data = request.session.get('pending_order_details')
            
            if not order_data:
                messages.error(request, 'Session data missing. Please try again.')
                return redirect('checkout')

            address = Address.objects.get(id=order_data['shipping_address_id'])
            coupon_id = order_data.get('coupon_id')
            coupon_discount=Decimal(order_data.get('coupon_price'))
            coupon = None
            if coupon_id:
                coupon = Coupon.objects.filter(coupon_id=coupon_id).first()

            order = Order.objects.create(
                user=request.user,
                payment_type='RazorPay',
                total_price=order_data.get('total_price'),
                payment_status=payment_status,
                shipping_address=address,
                offer_price=order_data.get('offer_price'),
                coupon_price=coupon_discount
            )

            cart = Cart.objects.get(user=request.user)
            cart_items = Cartitem.objects.filter(cart=cart)
            for item in cart_items:
                Order_items.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.product.price,
                    subtotal_price=(item.variant.product.price * item.quantity)-coupon_discount
                )

                item.variant.stock -= item.quantity
                item.variant.save()

            cart_items.delete()
            if coupon:
                Couponusage.objects.create(user=request.user, coupon=coupon, is_used=True)
                coupon.usage_count += 1
                coupon.save()

            if 'applied_coupon_id' in request.session:
                del request.session['applied_coupon_id']
            messages.success(request, 'Order placed! Payment status: {}'.format(payment_status))
            return redirect('order_confirmation')

        except razorpay.errors.SignatureVerificationError:
            order_data = request.session.get('pending_order_details')
            if not order_data:
                messages.error(request, 'Session data missing. Please try again.')
                return redirect('checkout')

            address = Address.objects.get(id=order_data['shipping_address_id'])
            payment_status = 'Failure'

            order = Order.objects.create(
                user=request.user,
                payment_type='RazorPay',
                total_price=order_data.get('total_price'),
                payment_status=payment_status,
                shipping_address=address,
            )

            cart = Cart.objects.get(user=request.user)
            cart_items = Cartitem.objects.filter(cart=cart)
            for item in cart_items:
                Order_items.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.product.price,
                    subtotal_price=(item.variant.product.price * item.quantity)-coupon_discount
                )

                item.variant.stock -= item.quantity
                item.variant.save()

            cart_items.delete()
            if 'applied_coupon_id' in request.session:
                del request.session['applied_coupon_id']

            messages.error(request, 'Payment verification failed. Please check your payment status.')
            return redirect('order_confirmation')

        
#================= Verify razorpay payment End===============# 


#========================Retry payment=======================# 
@never_cache
@login_required
def retry_payment(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    order_items = order.order_items.select_related('variant__product')

    if order.payment_status=='Success':
        return redirect('order_details')  
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        'amount': int(order.total_price * 100),
        'currency': "INR",
        'payment_capture': "1"
    })
    context = {
        'order': order,
        'order_items': order_items,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': order.total_price * 100
    }
    return render(request, 'user/retry_payment.html', context)


@never_cache
@login_required
def verify_retry_payment(request):
    if request.method == 'POST':
        user = request.user
        orders = Order.objects.filter(user=user)        
        order_id = request.POST.get('order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        try:
            order = Order.objects.get(order_id=order_id)
            order_items = Order_items.objects.filter(order=order)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            }
            client.utility.verify_payment_signature(params) 
            order.payment_status = 'Success'
            order.save()
            return redirect('order_confirmation')
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, 'Payment failed. Please try again.')
            return render(request, 'user/order_details.html', {'order': order, 'order_items': order_items, 'orders': orders})
    return HttpResponse("Invalid request method", status=400)


#=========================Retry payment End =======================# 

#========================= Order success===========================# 
@never_cache
@login_required(login_url='user_login')
def order_confirmation(request): 
    order=Order.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request,'user/order_confirmation.html',{'order':order})

#======================= Order success End=======================# 


#=========================Order_item cancel===========================# 
@never_cache
@login_required
def cancel_order_item(request, order_item_id):
    user = request.user
    order_item = get_object_or_404(Order_items, Orderitem_id=order_item_id, order__user=user)
    order = order_item.order
    final_price=0

    if order_item.status not in ['Delivered', 'Cancelled']:
        current_date=now().date()
        product=order_item.variant.product
        brand=product.brand
        product_offer=Product_offer.objects.filter(
            product=product,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()
        brand_offer=Brand_offer.objects.filter(
            brand=brand,
            started_date__lte=current_date,
            end_date__gte=current_date,
            status=True
        ).first()

        product_discount_price=None
        brand_disount_price=None

        if product_offer:
            product_discount_price=round(product.price * (1-(product_offer.offer_percentage/100)))

        if brand_offer:
            brand_disount_price=round(product.price * (1-(brand_offer.offer_percentage/100)))

        if product_discount_price is not None and brand_disount_price is not None:
            final_price=min(product_discount_price,brand_disount_price)
        elif product_discount_price is not None:
            final_price=product_discount_price
        elif brand_disount_price is not None:
            final_price=brand_disount_price
        else:
            final_price=product.price

        refund_amount=Decimal(final_price * order_item.quantity)

        if order.coupon_price>0:
            coupon_discount = round((order_item.subtotal_price/order.total_price) * order.coupon_price,0)
            refund_amount=refund_amount - coupon_discount
        if order.payment_status == 'Success':
            wallet, created = Wallet.objects.get_or_create(user=user)
            wallet.balance += refund_amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                details=f'Refund for canceled item in order #{order.tracking_number}',
                amount=refund_amount,
                transaction_type='Credit'
            )
            messages.success(
                request,
                f"₹{refund_amount} has been refunded to your wallet for the canceled item."
            )

        order_item.variant.stock = F('stock') + order_item.quantity
        order_item.variant.save()

        order_item.status = 'Cancelled'
        order_item.save()

        messages.success(
            request,
            f"Item {order_item.variant.product.name} from order #{order.tracking_number} has been canceled successfully."
        )
    else:
        messages.error(request, "Item cancellation failed. Delivered or already canceled items cannot be canceled.")

    return redirect('order_details')


#=========================Order cancel End=======================# 


#=========================Order Return===========================# 
@never_cache
@login_required
def return_order(request,orderitem_id):
    item=get_object_or_404(Order_items,Orderitem_id=orderitem_id)
    item.status='Requested Return'
    item.save()
    messages.success(request,f'Return request for order {item.order.tracking_number} has been submitted')
    return redirect('order_details')

#=========================Order Return End===========================# 


#=========================Generate Invoice===========================# 
def generate_invoice(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order_items=Order_items.objects.filter(order=order)
    html_content = render(request, 'user/invoice.html', {'order': order,'order_items':order_items}).content.decode('utf-8')
    
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.tracking_number}.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response

#=========================Generate Invoice End===========================# 
