from django.shortcuts import render,get_object_or_404,redirect
from . models import Coupon,Couponusage
from . validators import validate_coupon
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
from cart.models import Cart,Cartitem

# Create your views here.

#=================Coupon Managment===================
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def add_coupons(request):
    if request.method == 'POST':
        data = {
            'code': request.POST.get('code'),
            'description': request.POST.get('description'),
            'coupon_type': request.POST.get('coupon_type'),
            'discount_amount': request.POST.get('discount_amount'),
            'min_purchase_amount': request.POST.get('min_purchase_amount'),
            'valid_from': request.POST.get('valid_from'),
            'valid_to': request.POST.get('valid_to'),
            'usage_limit': request.POST.get('usage_limit'),
        }
        errors = validate_coupon(data)
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        Coupon.objects.create(
            code=data['code'],
            description=data['description'],
            coupon_type=data['coupon_type'],
            discount_amount=data['discount_amount'],
            min_purchase_amount=data['min_purchase_amount'],
            valid_from=data['valid_from'],
            valid_to=data['valid_to'],
            usage_limit=data['usage_limit'],
        )
        return JsonResponse({'success': True, 'message': 'Coupon added successfully'})
    return render(request, 'admin/add_coupons.html')


@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def edit_coupons(request, coupon_id):
    coupon = get_object_or_404(Coupon, coupon_id=coupon_id)
    if request.method == 'POST':
        data = {
            'code': request.POST.get('code'),
            'description': request.POST.get('description'),
            'coupon_type': request.POST.get('coupon_type'),
            'discount_amount': request.POST.get('discount_amount'),
            'min_purchase_amount': request.POST.get('min_purchase_amount'),
            'valid_from': request.POST.get('valid_from'),
            'valid_to': request.POST.get('valid_to'),
            'usage_limit': request.POST.get('usage_limit'),
        }
        errors = validate_coupon(data, coupon=coupon)
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        for key, value in data.items():
            setattr(coupon, key, value)
        coupon.save()
        return JsonResponse({'success': True, 'message': 'Coupon updated successfully'})
    return render(request, 'admin/edit_coupons.html', {'coupon': coupon})



def view_coupons(request):
    coupons =Coupon.objects.all()
    return render(request,'admin/coupons.html',{'coupons':coupons})

def activate_coupon(request,coupon_id):
    coupon=get_object_or_404(Coupon,coupon_id=coupon_id)
    coupon.is_active=True
    coupon.save()
    return redirect('view_coupons')


def deactivate_coupon(request,coupon_id):
    coupon=get_object_or_404(Coupon,coupon_id=coupon_id)
    coupon.is_active=False
    coupon.save()
    return redirect('view_coupons')


#=================Coupon Managment End===================#


@never_cache
def apply_coupon(request):
    if request.user.is_authenticated:
        user = request.user
        cart=get_object_or_404(Cart,user=user)
        cart_items=Cartitem.objects.filter(cart=cart)
        for cart_item in cart_items:
            variant=cart_item.variant
            product=variant.product
            
            discount_price=product.price
            cart_item.variant.product.price =discount_price
        if request.method == 'POST':
            code= request.POST.get('coupon_code','').strip()
            try:
                coupon = Coupon.objects.get(code__iexact=code)
            
                if not coupon.is_valid():
                    return JsonResponse({'success': False, 'message': 'Coupon is not valid or expired.'})

                if Couponusage.objects.filter(user=user, coupon=coupon).exists():
                    return JsonResponse({'success': False, 'message': 'Coupon already used.'})

                if not coupon.can_use():
                    return JsonResponse({'success': False, 'message': 'Coupon usage limit exceeded.'})

                total_amount = cart.total_price
                if total_amount < coupon.min_purchase_amount:
                    return JsonResponse({'success': False, 'message': 'Total amount does not meet the minimum purchase requirement.'})

                discount = coupon.calculate_discount(total_amount)
                discount_total = total_amount - discount

                Couponusage.objects.create(user=user, coupon=coupon)
                coupon.usage_count += 1
                coupon.save()

                print(discount_total)

                return JsonResponse({
                    'success': True,
                    'message': f'Coupon applied. You saved ₹{discount:.2f}',
                    'discount_total': f'{discount_total:.2f}'
                })

            except Coupon.DoesNotExist:
                print("Coupon not found.")
                return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})

            except Exception as e:
                print("Error:", str(e))  
                return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


                                    
            

    