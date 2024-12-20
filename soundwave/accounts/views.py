from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .form import Addressform,UserpasswordchangeFrom
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Address
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from user.models import CustomUser
from .validators import validate_first_name ,validate_last_name,validate_email,phone_validate
from orders.models import Order_items,Order


# Create your views here.


#=========================USER ACCOUNT VIEW==============================#
@login_required
def user_account_view(request):
    user=request.user
    context={
        'name':user.first_name +' '+ user.last_name,
        'email': user.email,
        'first_name':user.first_name,
        'last_name': user.last_name,
        'phone_number':user.phone_number,
    }
    return render(request,'user/user_account.html',context)


@login_required
def edit_details(request): 

    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=request.user.id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number', '') 
        
        errors = {}
        if first_name:
            first_name_error = validate_first_name(first_name)
            if first_name_error:
                errors['first_name'] = first_name_error

        if last_name:
            last_name_error = validate_last_name(last_name)
            if last_name_error:
                errors['last_name'] = last_name_error

        if phone_number:
            phone_number_error = phone_validate(phone_number, user_id=user.id)
            if phone_number_error:
                errors['phone_number'] = phone_number_error

        if email:
            email_error = validate_email(email)
            if email_error:
                errors['email'] = email_error
            if CustomUser.objects.filter(email__iexact=email).exclude(id=user.id).exists():
                errors['email_exists'] = 'Email already exists'

        if errors:
            return render(request, 'user/edit_personal_details.html', {'errors': errors,'first_name': first_name,'last_name': last_name,
                'email': email,
                'phone_number': phone_number,
            })

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.save()

        messages.success(request, 'Your details have been updated successfully.')
        return redirect('user_account')
    
    user = get_object_or_404(CustomUser, id=request.user.id)
    return render(request, 'user/edit_personal_details.html', {'user': user}) 

login_required
def change_password(request):
    user=request.user
    if request.method=='POST':
        form =UserpasswordchangeFrom(user=user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Your password has been sucessfully updated!')
            return redirect('user_account')
        else:
            messages.error(request,'Please correct the error and try again')
    else:
        form=UserpasswordchangeFrom(user=user)
    return render(request,'user/changepassword.html',{'form':form})





#=========================USER ACCOUNT VIEW End==============================#


#=========================USER ADDRESS VIEW,EDIT==============================#
@never_cache
@login_required
def add_address(request):
    if request.method=='POST':
        form =Addressform(request.POST)
        if form.is_valid():
            address =form.save(commit=False)
            address.user=request.user
            address.save()
            messages.success(request,'your address has been added successfully')
            return redirect('view_address')
        else:
            messages.error(request,'Please correct the form and try again.')
    else:
        form=Addressform()

    return render(request,'user/add_address.html',{'form':form})  

@never_cache
@login_required
def view_address(request):
    addresses=Address.objects.filter(user=request.user,is_active=True)
    return render(request,'user/address.html',{'addresses':addresses})


def order_list(request):
    status_filter = request.GET.get('status')
    if status_filter:
        orders = Order.objects.filter(order_items__status=status_filter, user=request.user)
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'user/order_details.html', {'orders': orders})


@never_cache
@login_required
def edit_address(request,address_id):
    address=get_object_or_404(Address,id=address_id)
    if request.method=='POST':
        form=Addressform(request.POST,instance=address)
        if form.is_valid():
            form.save()
            messages.success(request,'Address  update succussfully ')
            return redirect('view_address')
        else:
            messages.error(request,'Please Correct the form and try again ')
    else:
        form=Addressform(instance=address)
    return render(request,'user/edit_address.html',{'form':form})

@login_required(login_url='user_login')
def deactivate_address(request,address_id):
    address=get_object_or_404(Address,id=address_id)
    address.is_active=False
    address.save()
    return redirect('view_address')



#=========================USER ADDRESS VIEW,EDIT End==============================#


#=========================USER ORDER VIEW==============================#
@never_cache
@login_required(login_url='user_login')
def user_orders(request):
    orders = Order.objects.filter(user=request.user).select_related('shipping_address').prefetch_related('order_items__variant__product')
    return render(request, 'user/order_details.html', {'orders': orders})
