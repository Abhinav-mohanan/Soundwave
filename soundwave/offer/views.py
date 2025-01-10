from django.shortcuts import render,get_object_or_404,redirect
from . models import Brand_offer,Product_offer
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from products.models import Product,Brand
from django.http import JsonResponse
from decimal import Decimal,InvalidOperation
from datetime import datetime
from django.urls import reverse

# Create your views here.


#==================Product Offer====================#
@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def add_product_offer(request):
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        offer_percentage = request.POST.get('offer_percentage')
        product_id = request.POST.get('product')
        started_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        offer_details=request.POST.get('offer_details')

        errors = []
        if not offer_name:
            errors.append('Offer name is required.')
        if not offer_percentage:
            errors.append('Offer percentage is required.')
        if not product_id:
            errors.append('Please select a product.')
        if not started_date:
            errors.append('Start date is required.')
        if not end_date:
            errors.append('End date is required.')
        if not offer_details:
            errors.append('Offer details is required.')

        try:
            offer_percentage = Decimal(offer_percentage) if offer_percentage else None
            if offer_percentage and (offer_percentage <= 0 or offer_percentage > 75):
                errors.append('Offer price must be between 0 and 75 percentage.')
        except InvalidOperation:
            errors.append('Offer price must be a valid number.')

        try:
            started_date = datetime.strptime(started_date, '%Y-%m-%d').date() if started_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
            if started_date and end_date and started_date > end_date:
                errors.append('Start date cannot be after the end date.')
        except ValueError:
            errors.append('Invalid date format. Please use YYYY-MM-DD.')

        except Exception as e:
            errors.append(f'Error with production price:{str(e)}')

        if errors:
            return JsonResponse({'success': False, 'error': errors}, status=400)
    
        try:
            product = get_object_or_404(Product, id=product_id)
            Product_offer.objects.create(
                product=product,
                offer_name=offer_name,
                offer_percentage=offer_percentage,
                started_date=started_date,
                end_date=end_date,
                offer_details=offer_details
            )
            return JsonResponse({'success': True, 'message': 'Offer added successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': [str(e)]}, status=400)
    products = Product.objects.all()
    return render(request, 'admin/add_product_offer.html', {'products': products})


@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def edit_product_offer(request, product_offer_id):
    product_offer = get_object_or_404(Product_offer, id=product_offer_id)

    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        offer_percentage = request.POST.get('offer_percentage')
        product_id = request.POST.get('product')
        started_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        offer_details=request.POST.get('offer_details')

        errors = []
        if not offer_name:
            errors.append('Offer name is required.')
        if not offer_percentage:
            errors.append('Offer percentage is required.')
        if not product_id:
            errors.append('Please select a product.')
        if not started_date:
            errors.append('Start date is required.')
        if not end_date:
            errors.append('End date is required.')
        if not offer_details:
            errors.append('Offer details is required.')

        try:
            offer_percentage = Decimal(offer_percentage) if offer_percentage else None
            if offer_percentage and (offer_percentage <=0 and offer_percentage >75):
                errors.append('Offer price must be between 0 and 75 percentage.')
        except InvalidOperation:
            errors.append('Offer price must be a valid decimal number.')

        try:
            started_date = datetime.strptime(started_date, '%Y-%m-%d').date() if started_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
            if started_date and end_date and started_date > end_date:
                errors.append('Start date cannot be after the end date.')
        except ValueError:
            errors.append('Invalid date format. Please use YYYY-MM-DD.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        product=get_object_or_404(Product,id=product_id)
        product_offer.offer_name = offer_name
        product_offer.offer_percentage = offer_percentage
        product_offer.product = product
        product_offer.started_date = started_date
        product_offer.end_date = end_date
        product_offer.offer_details=offer_details
        product_offer.save()

        return JsonResponse({'success': True, 'message': 'Product offer updated successfully.'})
    products = Product.objects.all()
    return render(request, 'admin/edit_product_offer.html', {'products': products, 'product_offer': product_offer})


@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def activate_product_offer(request,product_offer_id):
    product_offer=get_object_or_404(Product_offer,id=product_offer_id)
    product_offer.status=True
    product_offer.save()
    return redirect(f"{reverse('view_offers')}?section=product")


@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def deactivate_product_offer(request,product_offer_id):
    product_offer=get_object_or_404(Product_offer,id=product_offer_id)
    product_offer.status=False
    product_offer.save()
    return redirect(f"{reverse('view_offers')}?section=product")


#==================Product Offer End====================#


#====================Brand Offer========================#
@never_cache
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def add_brand_offer(request):
    if request.method == 'POST':
    
        offer_name = request.POST.get('offer_name')
        offer_percentage = request.POST.get('offer_percentage')
        brand_id = request.POST.get('brand')
        started_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        offer_details=request.POST.get('offer_details')

        errors = []
        if not offer_name:
            errors.append('Offer name is required.')
        if not offer_percentage:
            errors.append('Offer percentage is required.')
        if not brand_id:
            errors.append('Please select a brand.')
        if not started_date:
            errors.append('Start date is required.')
        if not end_date:
            errors.append('End date is required.')
        if not offer_details:
            errors.append('Description is required.')

        try:
            offer_percentage = Decimal(offer_percentage) if offer_percentage else None
            if offer_percentage and (offer_percentage <=0 or offer_percentage>75):
                errors.append('Offer price must be between 0 and 75 percentage.')
        except InvalidOperation:
            errors.append('Offer price must be a valid decimal number.')

        try:
            started_date = datetime.strptime(started_date, '%Y-%m-%d').date() if started_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
            if started_date and end_date and started_date > end_date:
                errors.append('Start date cannot be after the end date.')
        except ValueError:
            errors.append('Invalid date format. Please use YYYY-MM-DD.')

        if errors:
            return JsonResponse({'success': False, 'error': errors}, status=400)

        try:
            brand = get_object_or_404(Brand, id=brand_id)
            Brand_offer.objects.create(
                brand=brand,
                offer_name=offer_name,
                offer_percentage=offer_percentage,
                started_date=started_date,
                end_date=end_date,
                offer_details=offer_details,
            )
            return JsonResponse({'success': True, 'message': 'Brand offer added successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': [str(e)]}, status=400)

    brands = Brand.objects.all()
    return render(request, 'admin/add_brand_offer.html', {'brands': brands})


@never_cache
@user_passes_test(lambda u:u.is_superuser,login_url='/adminn/')
def edit_brand_offer(request,brand_offer_id):
    brand_offer=get_object_or_404(Brand_offer,id=brand_offer_id)
    if request.method == 'POST':
        offer_name = request.POST.get('offer_name')
        offer_percentage = request.POST.get('offer_percentage')
        brand_id = request.POST.get('brand')
        started_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        offer_details = request.POST.get('offer_details')

        errors = []

        if not offer_name:
            errors.append('Offer name is required.')
        if not offer_percentage:
            errors.append('Offer price is required.')
        if not brand_id:
            errors.append('Please select a brand.')
        if not started_date:
            errors.append('Start date is required.')
        if not end_date:
            errors.append('End date is required.')
        if not offer_details:
            errors.append('Description is required.')

        try:
            offer_percentage = Decimal(offer_percentage) if offer_percentage else None
            if offer_percentage and (offer_percentage <=0 or offer_percentage>75):
                errors.append('Offer price must be between 0 and 75. percentage')
        except InvalidOperation:
            errors.append('Offer price must be a valid decimal number.')

        try:
            started_date = datetime.strptime(started_date, '%Y-%m-%d').date() if started_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
            if started_date and end_date and started_date > end_date:
                errors.append('Start date cannot be after the end date.')
        except ValueError:
            errors.append('Invalid date format. Please use YYYY-MM-DD.')
        if errors:
            return JsonResponse({'success': False, 'error': errors}, status=400)
        try:
            brand = get_object_or_404(Brand, id=brand_id)
            brand_offer.offer_name=offer_name
            brand_offer.offer_percentage=offer_percentage
            brand_offer.started_date=started_date
            brand_offer.end_date=end_date
            brand_offer.brand=brand
            brand_offer.offer_details=offer_details
            brand_offer.save()

            return JsonResponse({'success': True, 'message': 'Brand offer Updated successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': [str(e)]}, status=400)
    brands=Brand.objects.all()
    return render(request,'admin/edit_brand_offer.html',{'brand_offer':brand_offer,'brands':brands})     


@never_cache
@user_passes_test(lambda u:u.is_superuser,login_url='/adminn/')
def activate_brand_offer(request,brand_offer_id):
    brand_offer=get_object_or_404(Brand_offer,id=brand_offer_id)
    brand_offer.status=True
    brand_offer.save()
    return redirect('view_offers')


@never_cache
@user_passes_test(lambda u : u.is_superuser,login_url='/adminn/')
def deactivate_brand_offer(request,brand_offer_id):
    brand_offer =get_object_or_404(Brand_offer,id=brand_offer_id)
    brand_offer.status=False
    brand_offer.save()
    return redirect('view_offers')


#==================Brand Offer end====================#


#====================Offer View=======================#
@user_passes_test(lambda u: u.is_superuser, login_url='/adminn/')
def view_offer(request):
    product_offers=Product_offer.objects.all()
    brand_offers=Brand_offer.objects.all()
    return render(request,'admin/offer.html',{'product_offeres':product_offers,'brand_offers':brand_offers})