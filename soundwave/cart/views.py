from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart,Cartitem, Wishlist
from products.models import Variant
from django.views.decorators.cache import never_cache
from django.contrib import messages
import json
from offer.models import Brand_offer,Product_offer
from django.utils.timezone import now



#=====================Cart managment=======================#
@never_cache
@login_required(login_url='user_login')
def add_to_cart(request, variant_id):
    variant = get_object_or_404(
        Variant.objects.select_related("product"),
        id=variant_id,
        is_listed=True,
        stock__gte=0
    )
    if not variant.product.is_listed:
        messages.error(request, "This product is unavailable")
        return redirect('products')
    
    cart,_ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = Cartitem.objects.get_or_create(cart=cart, variant=variant)

    new_quantity = 1 if created else cart_item.quantity + 1

    if new_quantity > variant.stock:
        messages.error(request, f'Only {variant.stock} items available in stock')
        return redirect('cart_detail')
    
    cart_item.quantity = new_quantity
    cart_item.save()
    messages.success(request,'Product added to cart')
    return redirect('cart_detail')
    

@never_cache
@login_required
def remove_from_cart(request,cartitem_id):
    cart_item=get_object_or_404(Cartitem,cartitem_id=cartitem_id,cart__user=request.user)
    cart_item.delete()
    messages.info(request,'Product removerd from your cart')
    return redirect('cart_detail')


@never_cache
@login_required(login_url='user_login')
def update_cart_item(request, item_id):
    data = json.loads(request.body)
    quantity = data.get('quantity')

    if quantity is None or quantity < 1:
        return JsonResponse({'success': False, 'error': 'Invalid quantity'}, status=400)
    
    cart_item = get_object_or_404(
        Cartitem,
        cartitem_id=item_id,
        cart__user=request.user,
    )

    if quantity > cart_item.variant.stock:
        return JsonResponse({
            "success":False,
            "error": f"Only {cart_item.variant.stock} item(s) available in stock"
        },
        staus=400)
    cart_item.quantity = quantity
    cart_item.save()

    new_total = cart_item.total_price
    cart = cart_item.cart
    total_cart_price = cart.total_price

    return JsonResponse({
        "sucess": True,
        "new_total":new_total,
        "cart_total":total_cart_price
    })


@never_cache
@login_required(login_url='user_login')
def cart_detail(request):
    if 'applied_coupon_id' in request.session:
        del request.session['applied_coupon_id']
    cart,create=Cart.objects.get_or_create(user=request.user)
    cart_items=Cartitem.objects.filter(cart=cart)

    total=0
    

    current_date=now().date()

    for cart_item in cart_items:
        variant= cart_item.variant
        product=variant.product
        quantity=cart_item.quantity

        

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
            product_discount_price=(product.price * (1-(product_offer.offer_percentage/100)))
        
        if brand_offer:
            brand_discount_price=(product.price * (1-(brand_offer.offer_percentage/100)))

        if product_discount_price is not None and brand_discount_price is not None:
            final_discount_price = min(product_discount_price, brand_discount_price)
        elif product_discount_price is not None:
            final_discount_price = product_discount_price
        elif brand_discount_price is not None:
            final_discount_price = brand_discount_price
        else:
            final_discount_price = product.price

        cart_item.effective_price = round(final_discount_price, 0)
        cart_item.line_total = cart_item.effective_price * cart_item.quantity



        total=sum(item.line_total for item  in cart_items)

    return render(request,'user/cart.html',{'cart_items':cart_items,'total':total})


#=====================Cart managment End=======================#


#=====================Wishlist managment=======================#
@login_required(login_url='user_login')
def add_wishlist(request,variant_id):
    variant=get_object_or_404(Variant,id=variant_id)
    wishlist,created=Wishlist.objects.get_or_create(user=request.user,variant=variant)
    if created:
        messages.success(request,'Product added to your wishlist.')
    else:
        messages.info(request,'Item is already in your whislist.')
    return redirect('products')

@login_required(login_url='user_login')
def view_wishlist(request):
    user=request.user
    wishlist=Wishlist.objects.filter(user=user)
    return render(request,'user/wishlist.html',{'wishlist':wishlist})

@login_required(login_url='user_login')
def remove_from_wishlist(request,item_id):
    item=get_object_or_404(Wishlist,id=item_id,user=request.user)
    item.delete()
    messages.info(request,'Item removed from your whilist')
    return redirect('wishlist_details')



    
        

